import natural from 'natural';
import Sentiment from 'sentiment';

class FeedbackSystem {
  constructor() {
    this.sentiment = new Sentiment();
    this.tokenizer = new natural.WordTokenizer();
    this.tfidf = new natural.TfIdf();
  }

  analyzeResponse(response, context) {
    const sentimentAnalysis = this.analyzeSentiment(response);
    const keywordAnalysis = this.analyzeKeywords(response, context);
    const structureAnalysis = this.analyzeStructure(response);
    const actionableFeedback = this.generateActionableFeedback(sentimentAnalysis, keywordAnalysis, structureAnalysis);

    return {
      sentiment: sentimentAnalysis,
      keywords: keywordAnalysis,
      structure: structureAnalysis,
      feedback: actionableFeedback,
      overallScore: this.calculateOverallScore(sentimentAnalysis, keywordAnalysis, structureAnalysis)
    };
  }

  analyzeSentiment(response) {
    const result = this.sentiment.analyze(response);
    return {
      score: result.score,
      comparative: result.comparative,
      positive: result.positive,
      negative: result.negative
    };
  }

  analyzeKeywords(response, context) {
    this.tfidf.addDocument(context.jobDescription);
    this.tfidf.addDocument(response);

    const keywords = this.tokenizer.tokenize(response);
    return keywords.map(keyword => ({
      term: keyword,
      tfidf: this.tfidf.tfidf(keyword, 1)
    })).sort((a, b) => b.tfidf - a.tfidf).slice(0, 5);
  }

  analyzeStructure(response) {
    const sentences = response.split(/[.!?]+/);
    return {
      sentenceCount: sentences.length,
      averageWordCount: sentences.reduce((sum, sentence) => sum + this.tokenizer.tokenize(sentence).length, 0) / sentences.length
    };
  }

  generateActionableFeedback(sentiment, keywords, structure) {
    let feedback = [];

    if (sentiment.score < 0) {
      feedback.push("Consider using more positive language in your response.");
    }

    if (keywords.length < 3) {
      feedback.push("Try to incorporate more relevant keywords from the job description.");
    }

    if (structure.averageWordCount < 10) {
      feedback.push("Aim for more detailed responses with longer sentences.");
    }

    return feedback;
  }

  calculateOverallScore(sentiment, keywords, structure) {
    const sentimentScore = (sentiment.score + 5) / 10; // Normalize to 0-1
    const keywordScore = Math.min(keywords.length / 5, 1);
    const structureScore = Math.min(structure.averageWordCount / 20, 1);

    return (sentimentScore * 0.3 + keywordScore * 0.4 + structureScore * 0.3) * 100;
  }
}

export default FeedbackSystem;
