import { Box, Container, Paper, Stack } from "@mui/material";
import VerticalTabs from "./VerticalTabs";
import logo from "./assets/ImgHive_logo.png";


export default function App() {
  return (
    <Container maxWidth="md" sx={{ height: '100vh' }}>
      <Stack alignItems="strech" spacing={3}>
        <Box height={20}></Box>
        <Stack alignItems="center">
          <Box component="img" src={logo} sx={{ width: "30%" }} />
        </Stack>
        <Paper elevation={2} variant="outlined" sx={{borderRadius: 5}}>
          <VerticalTabs />
        </Paper>
      </Stack>
    </Container>
  )
}

