import { Box, Card, Stack, Typography } from "@mui/material"
import ImageGallery from "../components/ImageGallery";

export default function Browse() {
    return (
        <>
            <Stack spacing={3}>
                <Box>
                    <Typography variant="h5" gutterBottom>Browse User's Uploads</Typography>
                    <Typography variant="body2">Explore all images uploaded to the Hive.</Typography>
                    <Typography variant="body2">Use this page to scroll through thumbnails, open previews, and discover what's been added recently.</Typography>
                    <Typography variant="body2" gutterBottom>Images are displayed in order of upload time, newest first, and load automatically as you navigate.</Typography>
                </Box>

                <Stack alignItems="center">
                    <Card variant="outlined" sx={{ p: 3 }}>
                        <ImageGallery />
                    </Card>
                </Stack>
            </Stack>
        </>
    )
}
