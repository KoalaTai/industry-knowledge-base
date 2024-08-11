import SpeechToText from './speechToText.js';
import FeedbackSystem from './feedbackSystem.js';
import UserInterface from './userInterface.js';

class InterviewSimulation {
  constructor() {
    this.speechToText = new SpeechToText();
    this.feedbackSystem = new FeedbackSystem();
    this.userInterface = new UserInterface();
  }

  async startInterview(jobDescription, resume) {
    this.userInterface.renderInterviewUI();
    
    const audioStream = await this.userInterface.getAudioStream();
    
    this.speechToText.transcribe(audioStream).on('transcription', (transcription) => {
      this.userInterface.updateTranscription(transcription);
      
      const feedback = this.feedbackSystem.analyzeResponse(transcription, { jobDescription, resume });
      this.userInterface.updateFeedback(feedback);
    });
  }
}

export default InterviewSimulation;
