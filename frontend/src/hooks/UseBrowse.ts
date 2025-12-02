import { useQuery } from "@tanstack/react-query"
import { useState } from "react"

interface ImageDocument {
    id: string
    created_at: string
    status: string
    image_file_path: string | null
    thumbnail_file_path: string | null
}

interface ImagesResponse {
    page: number
    page_size: number
    total_items: number
    total_pages: number
    items: ImageDocument[]
}

export default function useBrowse() {
    
    const [page, setPage] = useState(1)

    const imagesQuery = useQuery({
        queryKey: ["images", page],
        queryFn: async () => {
            const response = await fetch(`http://localhost:8038/api/images?page=${page}&page_size=12&status=done&limit=20`)
            if (!response.ok) throw new Error(`Error: ${response.status} ${await response.text()}`)
            return response.json() as Promise<ImagesResponse>
        }
    })

    return { "page": page, "setPage": setPage, "isSuccess": imagesQuery.isSuccess, "data": imagesQuery.data }
}