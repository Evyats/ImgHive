import { ImageList, ImageListItem, Pagination, Stack } from "@mui/material"
import useBrowse from "../hooks/UseBrowse"



export default function ImageGallery() {
    
    const { page, setPage, isSuccess, data } = useBrowse()

    return (
        <>
            {
                isSuccess && data &&
                <Stack alignItems="center">
                    <Pagination
                        color="primary"
                        count={data.total_pages}
                        page={page}
                        onChange={(_, value) => { setPage(value) }} />
                    <ImageList rowHeight={130} cols={4} sx={{ width: 520 }}>
                        {data.items.map((item) => (
                            <ImageListItem key={item.id}>
                                <img
                                    src={`http://localhost:8038/api/images/${item.id}/thumbnail_file`}
                                    alt={item.id}
                                    loading="lazy"
                                />
                            </ImageListItem>
                        ))}
                    </ImageList>
                </Stack>
            }
        </>
    )
}
