import React, { useState, useEffect } from 'react';
import { Button, TextField, Paper, Typography } from '@material-ui/core';

const EnhancedUserInterface = ({ onStartInterview, onFeedback }) => {
  const [jobDescription, setJobDescription] = useState('');
  const [resume, setResume] = useState('');
  const [transcription, setTranscription] = useState('');
  const [feedback, setFeedback] = useState(null);

  useEffect(() => {
    if (feedback) {
      onFeedback(feedback);
    }
  }, [feedback, onFeedback]);

  const handleStartInterview = () => {
    onStartInterview(jobDescription, resume);
  };

  return (
    <Paper elevation={3} style={{ padding: '20px', maxWidth: '800px', margin: 'auto' }}>
      <Typography variant="h4" gutterBottom>
        AI-Powered Interview Assistant
      </Typography>
      <TextField
        fullWidth
        multiline
        rows={4}
        variant="outlined"
        label="Job Description"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
        margin="normal"
      />
      <TextField
        fullWidth
        multiline
        rows={4}
        variant="outlined"
        label="Your Resume"
        value={resume}
        onChange={(e) => setResume(e.target.value)}
        margin="normal"
      />
      <Button variant="contained" color="primary" onClick={handleStartInterview}>
        Start Interview
      </Button>
      {transcription && (
        <Paper elevation={1} style={{ marginTop: '20px', padding: '10px' }}>
          <Typography variant="h6">Live Transcription:</Typography>
          <Typography>{transcription}</Typography>
        </Paper>
      )}
      {feedback && (
        <Paper elevation={1} style={{ marginTop: '20px', padding: '10px' }}>
          <Typography variant="h6">Feedback:</Typography>
          <Typography>{feedback.sentiment.score > 0 ? 'Positive' : 'Needs Improvement'}</Typography>
          <Typography>Key Points: {feedback.keywords.map(k => k.term).join(', ')}</Typography>
          <Typography>Suggestions: {feedback.feedback.join(', ')}</Typography>
        </Paper>
      )}
    </Paper>
  );
};

export default EnhancedUserInterface;
