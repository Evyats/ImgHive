


interface ImagePreviewProps {
    thumbnail_url: string
    image_id: string
}
export default function ImagePreview({ thumbnail_url, image_id }: ImagePreviewProps) {
    return (
        <>
            <img
                src={thumbnail_url}
                alt={image_id}
                loading="lazy"
            />
        </>
    )
}