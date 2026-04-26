@'
/**
 * telegram-get-prompt
 * Wrapper that gets the system prompt for a Telegram topic
 * and returns it ready to prepend to a message
 */

module.exports = async (context, { topicId }) => {
  try {
    const fs = require('fs');
    const path = require('path');
    
    const promptsPath = path.join(
      process.env.OPENCLAW_WORKSPACE || 'C:\\Users\\User\\.openclaw\\workspace',
      'telegram-system-prompts.json'
    );
    
    if (!fs.existsSync(promptsPath)) {
      return {
        status: 'error',
        message: 'telegram-system-prompts.json not found',
        helpText: 'Copy telegram-system-prompts.json to workspace/'
      };
    }
    
    const promptsData = JSON.parse(fs.readFileSync(promptsPath, 'utf8'));
    const mainGroup = promptsData.groups.main_group;
    const topicData = mainGroup.topics[String(topicId)];
    
    if (!topicData) {
      return {
        status: 'error',
        message: `Topic ${topicId} not found`,
        availableTopics: Object.keys(mainGroup.topics).sort()
      };
    }
    
    return {
      status: 'ok',
      topicId: String(topicId),
      topicName: topicData.name,
      systemPrompt: topicData.systemPrompt,
      groupId: mainGroup.id,
      groupName: mainGroup.name,
      ready: true
    };
    
  } catch (error) {
    return {
      status: 'error',
      message: `Failed to load prompt: ${error.message}`,
      error: error.toString()
    };
  }
};
'@ | Set-Content "C:\Users\User\.openclaw\workspace\skills\telegram-get-prompt.js"

Write-Host "✓ Created telegram-get-prompt skill"