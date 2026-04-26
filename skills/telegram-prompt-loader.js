/**
 * telegram-prompt-loader
 * Loads system prompts for Telegram groups/topics
 * Usage: skill:telegram_prompt_loader topic=50
 */

module.exports = async (context, { topic }) => {
  try {
    const fs = require('fs');
    const path = require('path');
    
    const promptsPath = path.join(
      process.env.OPENCLAW_WORKSPACE || 'C:\\Users\\User\\.openclaw\\workspace',
      'telegram-system-prompts.json'
    );
    
    const promptsData = JSON.parse(fs.readFileSync(promptsPath, 'utf8'));
    
    // Get the main group (Agent HQ)
    const mainGroup = promptsData.groups.main_group;
    
    // Look up the topic
    const topicData = mainGroup.topics[topic];
    
    if (!topicData) {
      return {
        status: 'error',
        message: `Topic ${topic} not found in system prompts`,
        availableTopics: Object.keys(mainGroup.topics)
      };
    }
    
    return {
      status: 'ok',
      topicId: topic,
      topicName: topicData.name,
      systemPrompt: topicData.systemPrompt,
      groupName: mainGroup.name,
      groupId: mainGroup.id
    };
    
  } catch (error) {
    return {
      status: 'error',
      message: `Failed to load telegram prompts: ${error.message}`
    };
  }
};