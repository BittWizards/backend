import * as React from 'react';
import { styled } from '@mui/material/styles';
import Badge from '@mui/material/Badge';
import Avatar from '@mui/material/Avatar';

const SmallAvatar = styled(Avatar)(({ theme }) => ({
  width: 20,
  height: 20,
  border: `2px solid ${theme.palette.background.paper}`,
}));

export default function BadgeAvatars({avatar, achiev}) {
  return (
    <Badge
    overlap="circular"
    anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
    sx={{ marginTop: 3, marginBottom: 1, marginLeft: 3}}
    badgeContent={
      <SmallAvatar src="/static/images/avatar/1.jpg" />
    }
    >
      <Avatar src={avatar} sx={{ height: "100px", width: "100px" }} />
    </Badge>
  )
}
