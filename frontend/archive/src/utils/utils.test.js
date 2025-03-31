import { 
  formatTimestamp, 
  truncateText, 
  extractYoutubeId, 
  getYoutubeThumbnail,
  formatDate 
} from './index';

describe('Utility Functions', () => {
  describe('formatTimestamp', () => {
    test('formats seconds to HH:MM:SS', () => {
      expect(formatTimestamp(0)).toBe('00:00:00');
      expect(formatTimestamp(61)).toBe('00:01:01');
      expect(formatTimestamp(3661)).toBe('01:01:01');
      expect(formatTimestamp(7262)).toBe('02:01:02');
    });

    test('handles invalid input gracefully', () => {
      expect(formatTimestamp(null)).toBe('--:--:--');
      expect(formatTimestamp(undefined)).toBe('--:--:--');
      expect(formatTimestamp('')).toBe('--:--:--');
    });
  });

  describe('truncateText', () => {
    test('truncates text to the specified length', () => {
      const longText = 'This is a long text that needs to be truncated';
      expect(truncateText(longText, 10)).toBe('This is a...');
      expect(truncateText(longText, 20)).toBe('This is a long text...');
    });

    test('does not truncate text shorter than the limit', () => {
      const shortText = 'Short text';
      expect(truncateText(shortText, 20)).toBe(shortText);
    });

    test('uses default length if not specified', () => {
      const longText = 'a'.repeat(200);
      const result = truncateText(longText);
      expect(result.length).toBeLessThan(longText.length);
      expect(result.endsWith('...')).toBe(true);
    });

    test('handles invalid input gracefully', () => {
      expect(truncateText(null)).toBe('');
      expect(truncateText(undefined)).toBe('');
      expect(truncateText('')).toBe('');
    });
  });

  describe('extractYoutubeId', () => {
    test('extracts YouTube ID from various URL formats', () => {
      expect(extractYoutubeId('https://www.youtube.com/watch?v=dQw4w9WgXcQ')).toBe('dQw4w9WgXcQ');
      expect(extractYoutubeId('https://youtu.be/dQw4w9WgXcQ')).toBe('dQw4w9WgXcQ');
      expect(extractYoutubeId('https://youtube.com/embed/dQw4w9WgXcQ')).toBe('dQw4w9WgXcQ');
      expect(extractYoutubeId('https://youtube.com/v/dQw4w9WgXcQ')).toBe('dQw4w9WgXcQ');
    });

    test('returns null for invalid YouTube URLs', () => {
      expect(extractYoutubeId('https://example.com')).toBeNull();
      expect(extractYoutubeId('not a url')).toBeNull();
      expect(extractYoutubeId('')).toBeNull();
      expect(extractYoutubeId(null)).toBeNull();
    });
  });

  describe('getYoutubeThumbnail', () => {
    test('generates correct thumbnail URL from video ID', () => {
      const videoId = 'dQw4w9WgXcQ';
      expect(getYoutubeThumbnail(videoId)).toBe(`https://img.youtube.com/vi/${videoId}/mqdefault.jpg`);
    });

    test('returns empty string for invalid input', () => {
      expect(getYoutubeThumbnail('')).toBe('');
      expect(getYoutubeThumbnail(null)).toBe('');
      expect(getYoutubeThumbnail(undefined)).toBe('');
    });
  });

  describe('formatDate', () => {
    test('formats date strings to readable format', () => {
      const dateString = '2023-04-15T14:30:00Z';
      const result = formatDate(dateString);
      
      // We can't test the exact output as it depends on the locale,
      // but we can check that it returns a non-empty string
      expect(typeof result).toBe('string');
      expect(result.length).toBeGreaterThan(0);
      expect(result).toContain('2023');
      expect(result).toContain('Apr');
      expect(result).toContain('15');
    });

    test('handles invalid input gracefully', () => {
      expect(formatDate('')).toBe('');
      expect(formatDate(null)).toBe('');
      expect(formatDate(undefined)).toBe('');
    });
  });
}); 