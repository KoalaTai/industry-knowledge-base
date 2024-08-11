import fetch from 'node-fetch';
import NodeCache from 'node-cache';

class GPTIntegration {
  constructor() {
    this.apiKey = process.env.OPENAI_API_KEY;
    this.baseURL = 'https://api.openai.com/v1';
    this.cache = new NodeCache({ stdTTL: 600 });
    this.industryClassifier = new IndustryClassifier(); // Assume we have this class
  }

  async generateContent(context) {
    const cacheKey = JSON.stringify(context);
    const cachedResult = this.cache.get(cacheKey);
    if (cachedResult) return cachedResult;

    const industry = await this.industryClassifier.classify(context.jobDescription);
    const enhancedContext = this.enhanceContextWithIndustryTerms(context, industry);

    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    };

    const body = {
      model: "gpt-4",
      messages: [
        { role: "system", content: `You are an AI assistant specialized in ${industry} interviews. Use industry-specific terminology where appropriate.` },
        { role: "user", content: this.buildPrompt(enhancedContext) }
      ],
      max_tokens: 150,
      temperature: 0.7
    };

    try {
      const response = await fetch(`${this.baseURL}/chat/completions`, {
        method: 'POST',
        headers: headers,
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data = await response.json();
      const result = data.choices[0].message.content.trim();
      this.cache.set(cacheKey, result);
      return result;
    } catch (error) {
      console.error("Error in GPT integration:", error);
      throw error;
    }
  }

  enhanceContextWithIndustryTerms(context, industry) {
    // This method would add industry-specific terms to the context
    // Implementation depends on how we store and retrieve industry-specific terms
    return {
      ...context,
      industry: industry
    };
  }

  buildPrompt(context) {
    return `Given the following job description: "${context.jobDescription}" 
            and resume: "${context.resume}", 
            provide a ${context.industry}-specific interview question and guidance 
            for the topic: ${context.topic}`;
  }
}

export default GPTIntegration;
