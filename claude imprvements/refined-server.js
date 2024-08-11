import Authentication from './authentication.js';
import DataProtection from './dataProtection.js';
import SpeechToText from './speechToText.js';
import GPTIntegration from './gptIntegration.js';
import UserInterface from './userInterface.js';
import FeedbackSystem from './feedbackSystem.js';

class Server {
  constructor(expressApp) {
    this.app = expressApp;
    this.authentication = new Authentication();
    this.dataProtection = new DataProtection();
    this.speechToText = new SpeechToText();
    this.gptIntegration = new GPTIntegration();
    this.userInterface = new UserInterface();
    this.feedbackSystem = new FeedbackSystem();
    this.masterKey = this.dataProtection.generateMasterKey();
  }

  async handleRequests() {
    this.app.post('/login', async (req, res) => {
      try {
        const token = await this.authentication.login(req.body);
        res.json({ token });
      } catch (error) {
        res.status(401).json({ error: error.message });
      }
    });

    this.app.post('/register', async (req, res) => {
      try {
        const hashedPassword = await this.dataProtection.hashPassword(req.body.password);
        const result = await this.authentication.register({ ...req.body, password: hashedPassword });
        res.json({ message: 'Registration successful' });
      } catch (error) {
        res.status(400).json({ error: error.message });
      }
    });

    this.app.post('/interview', async (req, res) => {
      try {
        const encryptedContext = this.dataProtection.encrypt(JSON.stringify(req.body), this.masterKey);
        const audioStream = await this.speechToText.getAudioStream(req);
        const transcription = await this.speechToText.transcribe(audioStream);
        const decryptedContext = JSON.parse(this.dataProtection.decrypt(encryptedContext, this.masterKey));
        const gptResponse = await this.gptIntegration.generateContent({ ...decryptedContext, transcription });
        const feedback = this.feedbackSystem.analyzeResponse(transcription, decryptedContext);
        res.json({ gptResponse, feedback });
      } catch (error) {
        res.status(500).json({ error: error.message });
      }
    });

    // Other routes...
  }

  start() {
    const port = process.env.PORT || 3000;
    this.app.listen(port, () => {
      console.log(`Server is running on port ${port}`);
    });
  }
}

export default Server;
