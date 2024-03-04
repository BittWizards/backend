import React from 'react'
import Button from '@mui/material/Button'

export default function ButtonComponent(props) {
    return (
        <Button {...props}
            sx={{
            background: '#512da8',
            textTransform: 'none',
            fontFamily: 'YSText',
            fontWeight: 500,
            fontSize: 18,
            lineHeight: 1.2,
            padding: 0,
            width: "30px",
            height: "30px",
            '&:hover': {
              background: '#47298E',
            },
            '&:active': {
              background: '#341c6c',
            },
            '&:disabled': {
              cursor: 'auto',
            },
          }}
          variant="contained"/>
    )
}
