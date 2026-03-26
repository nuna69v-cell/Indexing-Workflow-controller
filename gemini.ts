import { Command } from 'commander';
import chalk from 'chalk';
import { GoogleGenAI } from "@google/genai";
import dotenv from 'dotenv';

dotenv.config();

const program = new Command();

program
  .name('gemini')
  .description('Gemini CLI - GenX VisionOps AI Assistant')
  .version('1.0.0');

program
  .command('ask <prompt>')
  .description('Ask Gemini a question')
  .action(async (prompt: string) => {
    console.log(chalk.blue(`Asking Gemini: ${prompt}...`));
    try {
      const apiKey = process.env.GEMINI_API_KEY;
      if (!apiKey) {
        console.error(chalk.red('GEMINI_API_KEY not found in environment.'));
        return;
      }
      const ai = new GoogleGenAI({ apiKey });
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: prompt,
      });
      console.log(chalk.green('Gemini Response:'));
      console.log(response.text);
    } catch (error) {
      console.error(chalk.red('Failed to get response from Gemini.'));
      console.error(error);
    }
  });

program
  .command('analyze <symbol>')
  .description('Analyze market data for a symbol')
  .action(async (symbol: string) => {
    console.log(chalk.blue(`Analyzing market data for ${symbol}...`));
    try {
      const apiKey = process.env.GEMINI_API_KEY;
      if (!apiKey) {
        console.error(chalk.red('GEMINI_API_KEY not found in environment.'));
        return;
      }
      const ai = new GoogleGenAI({ apiKey });
      const prompt = `Analyze the current market sentiment and potential price action for ${symbol} in the context of GenX VisionOps trading strategies.`;
      const response = await ai.models.generateContent({
        model: "gemini-3-flash-preview",
        contents: prompt,
      });
      console.log(chalk.green('Market Analysis:'));
      console.log(response.text);
    } catch (error) {
      console.error(chalk.red('Failed to analyze market data.'));
    }
  });

program.parse(process.argv);
