/**
 * Utilities index file
 * Exports all utility functions and constants for easy imports
 */

/**
 * Format a timestamp (in seconds) to a readable format (HH:MM:SS)
 * @param {number} seconds - Time in seconds
 * @returns {string} - Formatted time string
 */
export const formatTimestamp = (seconds) => {
  if (!seconds && seconds !== 0) return '--:--:--';
  
  const hours = Math.floor(seconds / 3600);
  const minutes = Math.floor((seconds % 3600) / 60);
  const secs = Math.floor(seconds % 60);
  
  return [
    hours.toString().padStart(2, '0'),
    minutes.toString().padStart(2, '0'),
    secs.toString().padStart(2, '0')
  ].join(':');
};

/**
 * Truncate text to a specified length with ellipsis
 * @param {string} text - Text to truncate
 * @param {number} maxLength - Maximum length before truncation
 * @returns {string} - Truncated text with ellipsis if needed
 */
export const truncateText = (text, maxLength = 100) => {
  if (!text) return '';
  if (text.length <= maxLength) return text;
  
  return text.substring(0, maxLength).trim() + '...';
};

/**
 * Extract YouTube video ID from various URL formats
 * @param {string} url - YouTube URL
 * @returns {string|null} - YouTube video ID or null if invalid
 */
export const extractYoutubeId = (url) => {
  if (!url) return null;
  
  // Regular expression to match YouTube video ID from various URL formats
  const regExp = /^.*(youtu.be\/|v\/|e\/|u\/\w+\/|embed\/|v=)([^#&?]*).*/;
  const match = url.match(regExp);
  
  return (match && match[2].length === 11) ? match[2] : null;
};

/**
 * Generate a YouTube thumbnail URL from a video ID
 * @param {string} videoId - YouTube video ID
 * @returns {string} - URL to the video thumbnail
 */
export const getYoutubeThumbnail = (videoId) => {
  if (!videoId) return '';
  return `https://img.youtube.com/vi/${videoId}/mqdefault.jpg`;
};

/**
 * Format a date string to a more readable format
 * @param {string} dateString - ISO date string
 * @returns {string} - Formatted date
 */
export const formatDate = (dateString) => {
  if (!dateString) return '';
  
  const options = { 
    year: 'numeric', 
    month: 'short', 
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  };
  
  return new Date(dateString).toLocaleDateString('en-US', options);
}; 