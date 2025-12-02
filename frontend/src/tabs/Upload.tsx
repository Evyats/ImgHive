import { Alert, Box, Card, Chip, CircularProgress, Divider, Stack, Typography } from "@mui/material"
import InputFileUpload from "../components/InputFileUpload"
import { useEffect, useState } from "react";
import Thumbnail from "../components/Thumbnail";
import { useMutation, useQuery } from "@tanstack/react-query";
import SendButton from "../components/SendButton";




interface UploadResponse {
    id: string;
    status: "queued" | "processing" | "done" | "failed";
    polling: string;
    creation_time: string;
}


interface StatusResponse {
    image_id: string,
    status: "queued" | "processing" | "done" | "failed",
}


export default function Upload() {

    const [fileToUpload, setFileToUpload] = useState<File | undefined>(undefined)
    const [fileUrl, setFileUrl] = useState<string | undefined>(undefined)
    const [imageId, setImageId] = useState<string | undefined>(undefined)
    const [loading, setLoading] = useState<string | null>(null)
    const [error, setError] = useState<string | null>(null)




    function handleUpload(event: React.ChangeEvent<HTMLInputElement>) {
        const file = event.target.files?.[0];
        setFileToUpload(file)
        if (file) {
            const url = URL.createObjectURL(file);
            setFileUrl(url)
        }
    }

    // mutate, data, isPending, isError, error, isSuccess
    const upload = useMutation<UploadResponse, Error, File>({
        mutationFn: async (file) => {
            const form = new FormData();
            form.append("file", file);
            const result = await fetch("http://localhost:8038/api/images", { method: "POST", body: form, });

            if (!result.ok) {
                const text = await result.text();
                throw new Error(`Upload failed: ${result.status} ${text}`);
            }

            const uploadResponse = (await result.json()) as UploadResponse;
            return uploadResponse
        },
        onSuccess: (data) => {
            setImageId(data.id);
        },
    });

    const handleSend = () => {
        if (fileToUpload) upload.mutate(fileToUpload);
    };



    // data: status, isLoading, isError, error
    const polling = useQuery({
        queryKey: ["status", imageId],
        queryFn: async () => {
            const res = await fetch(`http://localhost:8038/api/images/${imageId}/status`);
            if (!res.ok) throw new Error("status failed");
            return res.json() as Promise<StatusResponse>;
        },
        enabled: !!imageId,
        refetchInterval: (query) => {
            const data = query.state.data;
            const pollDelay = 1000
            if (!data) return pollDelay;
            if (data.status === "done" || data.status === "failed") {
                // if (data.status === "done") setImageReady(true)
                return false;
            }
            return pollDelay;
        },
    });



    // data, isLoading, isError, error
    const resultImage = useQuery({
        queryKey: ["image-file", imageId],
        enabled: polling.data?.status === "done",
        queryFn: async () => {
            const result = await fetch(`http://localhost:8038/api/images/${imageId}/image_file`);
            if (!result.ok) throw new Error("failed loading image file");
            const blob = await result.blob();
            return URL.createObjectURL(blob);
        },
    });




    useEffect(() => {
        if (upload.isPending) {
            setLoading("Uploading")
        }
        else if (polling.data?.status === "queued") {
            setLoading("Waiting in queue")

        }
        else if (polling.data?.status === "processing") {
            setLoading("Processing")

        }
        else {
            setLoading(null)
        }
    }, [upload.isPending, polling.data?.status])




    useEffect(() => {
        if (upload.isError) {
            setError(upload.error.message)
        }
        else if (polling.isError) {
            setError(polling.error.message)
        }
        else {
            setError(null)
        }

    }, [upload.isError, polling.isError])




    return (
        <>

            <Stack spacing={3}>

                <Stack direction="row" spacing={2}>
                    <Box sx={{ flex: 1 }}>
                        <Typography variant="h5" gutterBottom>Upload</Typography>
                        <Typography variant="body2" gutterBottom>
                            Choose a picture from your device and preview it before sending.
                            We'll process it automatically, create a clean thumbnail, and add it to your Hive for browsing later.
                        </Typography>
                    </Box>

                    <Divider orientation="vertical" flexItem />

                    <Stack alignItems="center" spacing={2} sx={{ flex: 1 }}>
                        <InputFileUpload disabled={loading != null} handleUpload={handleUpload} />
                        <Thumbnail url={fileUrl} squareSize={100} />
                        <SendButton disabled={!fileUrl || (loading != null)} onSend={handleSend} />
                    </Stack>
                </Stack>


                <Box>
                    {
                        loading &&
                        <Alert severity="info" icon={false}>
                            <Stack direction="row" alignItems="center" spacing={2}>
                                <CircularProgress size={15} />
                                <Box>{loading} . . .</Box>
                            </Stack>
                        </Alert>
                    }
                    {
                        error &&
                        <Alert severity="error" >
                            Something went wrong: {error}
                        </Alert>
                    }
                    {
                        polling.data?.status === "done" &&
                        <Alert severity="success" >
                            Image uploaded successfully!
                        </Alert>
                    }
                </Box>


                <Stack alignItems="center">
                    {
                        resultImage.data &&
                        <Card variant="outlined" sx={{ maxWidth: 400 }}>
                            <Box padding={2}>
                                <img src={resultImage.data} style={{ width: "100%" }} />
                            </Box>
                            <Divider />
                            <Box padding={2} >
                                <Typography gutterBottom variant="body2">Generated URL of the image:</Typography>
                                <Stack direction="row" spacing={1}>
                                    <Chip label={`http://localhost:8038/api/images/${upload.data?.id}/image_file`} size="small" />
                                </Stack>
                            </Box>
                        </Card>
                    }
                </Stack>


            </Stack>


        </>
    )
}
