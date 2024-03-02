import * as React from 'react';
import { styled } from '@mui/material/styles';
import Tabs from '@mui/material/Tabs';
import Tab from '@mui/material/Tab';

const tabsList = [
  {value: "profile", label: "Profile"},
  {value: "achievements", label: "Achievements"},
  {value: "statistic", label: "Statistic"},
]

const CustomTabs = styled(Tabs)({
  // borderBottom: '1px solid #e8e8e8',
  '& .MuiTabs-indicator': {
    backgroundColor: '#1890ff',
  },
});


const CustomTab = styled((props) => <Tab disableRipple {...props} />)(({ theme }) => ({
  textTransform: 'none',
  minWidth: 0,
  [theme.breakpoints.up('sm')]: {
    minWidth: 0,
  },
  fontWeight: theme.typography.fontWeightRegular,
  fontSize: "large",
  marginRight: theme.spacing(1),
  color: 'rgba(0, 0, 0, 0.85)',
  fontFamily: [
    '-apple-system',
    'BlinkMacSystemFont',
    '"Segoe UI"',
    'Roboto',
    '"Helvetica Neue"',
    'Arial',
    'sans-serif',
    '"Apple Color Emoji"',
    '"Segoe UI Emoji"',
    '"Segoe UI Symbol"',
  ].join(','),
  '&:hover': {
    color: '#2434C0',
    opacity: 1,
  },
  '&.Mui-selected': {
    color: '#2434C0',
    fontWeight: theme.typography.fontWeightMedium,
  },
  '&.Mui-focusVisible': {
    backgroundColor: '#d1eaff',
  },
}));


export default function ColorTabs({onClick, currentTab}) {

  const handleChange = (event, newValue) => {
    onClick(newValue);
  };

  return (
    <CustomTabs
    value={currentTab}
    onChange={handleChange}
    textColor="inherit"
    indicatorColor="primary"
    aria-label="Nav bar"
    role="navigation"
    centered="true"
    >
        {tabsList.map(tab => (<CustomTab {...tab} />))}
    </CustomTabs>
  );
}
