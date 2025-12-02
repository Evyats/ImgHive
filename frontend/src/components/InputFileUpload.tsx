import { styled } from '@mui/material/styles';
import Button from '@mui/material/Button';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import { useState } from 'react';


const VisuallyHiddenInput = styled('input')({
    clip: 'rect(0 0 0 0)',
    clipPath: 'inset(50%)',
    height: 1,
    overflow: 'hidden',
    position: 'absolute',
    bottom: 0,
    left: 0,
    whiteSpace: 'nowrap',
    width: 1,
});




interface InputFileUploadProps {
    handleUpload: (event: React.ChangeEvent<HTMLInputElement>) => void
    disabled: boolean
}
export default function InputFileUpload({ handleUpload, disabled }: InputFileUploadProps) {

    return (
        <Button
            size="small"
            component="label"
            role={undefined}
            variant="contained"
            tabIndex={-1}
            startIcon={<CloudUploadIcon />}
            disableElevation
            disabled={disabled}
        >
            Browse
            <VisuallyHiddenInput
                type="file"
                accept="image/*"
                onChange={handleUpload}
            />
        </Button>
    );
}
