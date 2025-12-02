import { Button } from "@mui/material";
import SendIcon from "@mui/icons-material/Send";


interface SendButtonProps {
    disabled?: boolean;
    onSend: () => void;
}

export default function SendButton({ disabled, onSend }: SendButtonProps) {
    return (
        <Button
            size="small"
            startIcon={<SendIcon />}
            variant="contained"
            disabled={disabled}
            disableElevation
            onClick={onSend}
        >
            Send!
        </Button>
    );
}
