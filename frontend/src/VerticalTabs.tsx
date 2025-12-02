import * as React from 'react';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';
import Box from '@mui/material/Box';
import Home from './tabs/Home';
import Upload from './tabs/Upload';
import Browse from './tabs/Browse';
import { Stack } from '@mui/material';


interface TabPanelProps {
    children?: React.ReactNode;
    index: number;
    value: number;
}
function TabPanel(props: TabPanelProps) {
    const { children, value, index } = props;
    return (
        <div hidden={value !== index} style={{ width: "100%" }}>
            {value === index && (
                <Box sx={{ p: 3 }}>{children}</Box>
            )}
        </div>
    );
}


export default function VerticalTabs() {
    const [value, setValue] = React.useState(0);

    return (
        // <Box sx={{ flexGrow: 1, bgcolor: 'background.paper', display: 'flex'}}>
        <Stack direction="row" alignItems="strech" sx={{ bgcolor: 'grey.50', borderRadius: 5 }}>
            <Tabs
                orientation="vertical"
                variant="scrollable"
                value={value}
                onChange={(_, newValue: number) => { setValue(newValue) }}
                sx={{ borderRight: 1, borderColor: 'divider', flexShrink: 0 }}
            >
                <Tab label="Home" />
                <Tab label="Upload" />
                <Tab label="Browse" />
            </Tabs>
            <TabPanel value={value} index={0}>
                <Home />
            </TabPanel>
            <TabPanel value={value} index={1}>
                <Upload />
            </TabPanel>
            <TabPanel value={value} index={2}>
                <Browse />
            </TabPanel>
        </Stack>
    );
}

