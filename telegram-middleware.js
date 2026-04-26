/**
 * Telegram Message Middleware
 * Intercepts incoming Telegram messages and loads topic system prompts
 */

module.exports = async (gateway, message) => {
  // Only process Telegram messages
  if (message.source !== 'telegram') return message;
  
  // Extract topic ID
  const topicId = message.topicId || message.chatId;
  if (!topicId) return message; // Not a topic message
  
  try {
    // Load the system prompt for this topic
    const promptLoader = require('./skills/telegram-prompt-loader.js');
    const promptResult = await promptLoader(null, { topic: String(topicId) });
    
    if (promptResult.status === 'ok') {
      // Attach system prompt to message context
      message.systemPrompt = promptResult.systemPrompt;
      message.topicName = promptResult.topicName;
      message.systemPromptLoaded = true;
      
      console.log(`✓ Loaded prompt for topic ${topicId} (${promptResult.topicName})`);
    } else {
      console.warn(`⚠ Failed to load prompt for topic ${topicId}: ${promptResult.message}`);
    }
  } catch (error) {
    console.error(`✗ Middleware error for topic ${topicId}: ${error.message}`);
  }
  
  return message;
};