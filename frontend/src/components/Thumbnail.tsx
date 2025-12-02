import { Box } from "@mui/material"

export default Thumbnail

interface ThumbnailProps {
    url: string | undefined
    squareSize: number
}
function Thumbnail({ url, squareSize }: ThumbnailProps) {
    return (
        <Box sx={{ width: squareSize, height: squareSize, overflow: 'hidden', borderRadius: "50%", border: 1 }}>
            <img
                src={url}
                style={{
                    width: "100%",
                    height: "100%",
                    objectFit: "cover",   // fills + crops to square
                    objectPosition: "center",
                }}
            />
        </Box>
    )
}