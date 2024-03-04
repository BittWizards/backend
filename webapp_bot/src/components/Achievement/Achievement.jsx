import * as React from 'react';
import PropTypes from 'prop-types';
import { styled } from '@mui/material/styles';
import Stepper from '@mui/material/Stepper';
import Step from '@mui/material/Step';
import StepLabel from '@mui/material/StepLabel';
import Check from '@mui/icons-material/Check';
import StepConnector, { stepConnectorClasses } from '@mui/material/StepConnector';
import EmojiEventsIcon from '@mui/icons-material/EmojiEvents';

const QontoConnector = styled(StepConnector)(({ theme }) => ({
  marginTop: 10,
  marginBottom: 10,
  [`&.${stepConnectorClasses.alternativeLabel}`]: {
    left: 10,
    top: 'calc(-50% + 16px)',
    bottom: 'calc(50% + 16px)',
  },
  [`&.${stepConnectorClasses.active}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      borderColor: '#E8A043',
    },
  },
  [`&.${stepConnectorClasses.completed}`]: {
    [`& .${stepConnectorClasses.line}`]: {
      borderColor: '#60BAA2',
    },
  },
  [`& .${stepConnectorClasses.line}`]: {
    borderColor: theme.palette.mode === 'dark' ? theme.palette.grey[800] : '#eaeaf0',
    borderTopWidth: 3,
    borderRadius: 1,
  },
}));

const QontoStepIconRoot = styled('div')(({ theme, ownerState }) => ({
  color: theme.palette.mode === 'dark' ? theme.palette.grey[700] : '#eaeaf0',
  display: 'flex',
  height: 22,
  alignItems: 'center',
  ...(ownerState.active && {
    color: '#E8A043',
  }),
  '& .QontoStepIcon-completedIcon': {
    color: '#60BAA2',
    zIndex: 1,
    fontSize: 18,
    marginLeft: -4,
  },
  '& .QontoStepIcon-circle': {
    width: 8,
    height: 8,
    borderRadius: '50%',
    backgroundColor: 'currentColor',
  },
}));

function QontoStepIcon(props) {
  const { active, completed, className } = props;

  const icons = {
    1: <div className="QontoStepIcon-circle" />,
    2: <div className="QontoStepIcon-circle" />,
    3: <EmojiEventsIcon sx={{ marginLeft: -2, height: 40, width: 40 }}/>,
  }

  return (
    <QontoStepIconRoot ownerState={{ active }} className={className}>
      {completed ? (
        <Check className="QontoStepIcon-completedIcon" />
      ) : (
        icons[String(props.icon)]
        // <div className="QontoStepIcon-circle" />
      )}
    </QontoStepIconRoot>
  );
}

QontoStepIcon.propTypes = {
  /**
   * Whether this step is active.
   * @default false
   */
  active: PropTypes.bool,
  className: PropTypes.string,
  /**
   * Mark the step as completed. Is passed to child components.
   * @default false
   */
  completed: PropTypes.bool,
};

const steps = [
  'Select master blaster campaign settings',
  'Create an ad group',
  'Create an ad',
];

export default function HorizontalLinearAlternativeLabelStepper() {
  return (
    <Stepper activeStep={1} connector={<QontoConnector />} orientation='vertical' sx={{ marginLeft: 5, marginTop: 5 }}>
      {steps.map((label) => (
        <Step key={label}>
          <StepLabel StepIconComponent={QontoStepIcon} sx={{ marginLeft: 1 }}>{label}</StepLabel>
        </Step>
      ))}
    </Stepper>
  );
}
