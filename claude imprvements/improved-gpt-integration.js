import fetch from 'node-fetch';
import NodeCache from 'node-cache';

class GPTIntegration {
  constructor() {
    this.apiKey = process.env.OPENAI_API_KEY;
    this.baseURL = 'https://api.openai.com/v1';
    this.cache = new NodeCache({ stdTTL: 600 }); // Cache with 10-minute TTL
    this.maxRetries = 3;
  }

  async generateContent(context) {
    const cacheKey = JSON.stringify(context);
    const cachedResult = this.cache.get(cacheKey);
    if (cachedResult) return cachedResult;

    const headers = {
      'Authorization': `Bearer ${this.apiKey}`,
      'Content-Type': 'application/json'
    };

    const body = {
      model: "gpt-4",
      messages: [{ role: "user", content: this.buildPrompt(context) }],
      max_tokens: context.max_tokens || 150,
      temperature: context.temperature || 0.7,
      top_p: context.top_p || 1,
      frequency_penalty: context.frequency_penalty || 0,
      presence_penalty: context.presence_penalty || 0
    };

    for (let attempt = 1; attempt <= this.maxRetries; attempt++) {
      try {
        const response = await fetch(`${this.baseURL}/chat/completions`, {
          method: 'POST',
          headers: headers,
          body: JSON.stringify(body)
        });

        if (!response.ok) {
          const errorData = await response.json();
          throw new Error(`HTTP error! status: ${response.status}, message: ${errorData.error.message}`);
        }

        const data = await response.json();
        const result = data.choices[0].message.content.trim();
        this.cache.set(cacheKey, result);
        return result;
      } catch (error) {
        console.error(`Attempt ${attempt} failed:`, error);
        if (attempt === this.maxRetries) throw error;
      }
    }
  }

  buildPrompt(context) {
    // Enhance prompt building to handle industry-specific terminology
    let prompt = `Context: ${context.jobDescription}\n\n`;
    prompt += `User resume: ${context.resume}\n\n`;
    prompt += `Based on the job description and resume, provide an interview question and guidance for the following topic: ${context.topic}`;
    return prompt;
  }
}

export default GPTIntegration;
