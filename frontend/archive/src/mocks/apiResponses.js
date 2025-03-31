/**
 * Mock API responses for testing frontend components
 * These are used to simulate API responses before backend is connected
 */

// Mock transcript list
export const mockTranscripts = [
  { 
    id: '1', 
    title: 'Introduction to AI', 
    url: 'https://www.youtube.com/watch?v=abc123',
    createdAt: '2023-04-15', 
    status: 'completed',
    audioStatus: 'completed',
    audioUrl: 'https://example.com/audio/transcript_1.mp3'
  },
  { 
    id: '2', 
    title: 'Machine Learning Fundamentals', 
    url: 'https://www.youtube.com/watch?v=def456',
    createdAt: '2023-05-20', 
    status: 'completed',
    audioStatus: null
  },
  { 
    id: '3', 
    title: 'Neural Networks Explained', 
    url: 'https://www.youtube.com/watch?v=ghi789',
    createdAt: '2023-06-10', 
    status: 'processing',
    audioStatus: null
  },
];

// Mock transcript detail
export const mockTranscriptDetail = {
  id: '1',
  title: 'Introduction to AI',
  date: '2023-04-15',
  status: 'processed',
  youtubeId: 'abc123',
  url: 'https://www.youtube.com/watch?v=abc123',
  duration: 35, // minutes
  content: `Welcome to this introduction to Artificial Intelligence. Today, we'll be exploring the fundamentals of AI, its history, and its applications in the modern world.

AI, or Artificial Intelligence, refers to the simulation of human intelligence in machines that are programmed to think and learn like humans. The term was coined in 1956 by John McCarthy, who defined it as "the science and engineering of making intelligent machines."

The field of AI has evolved significantly since its inception. Early AI research focused on problem-solving and symbolic methods. By the early 21st century, machine learning had become the dominant approach, with deep learning emerging as a particularly effective technique.

There are different types of AI, including:
1. Narrow AI: AI that is designed to perform a specific task, like voice recognition.
2. General AI: AI that can perform any intellectual task that a human being can do.
3. Superintelligent AI: AI that surpasses human intelligence and ability.

Applications of AI are widespread and include virtual assistants like Siri and Alexa, recommendation systems used by platforms like Netflix and Amazon, autonomous vehicles, and more advanced applications in healthcare, finance, and many other sectors.

As we delve deeper into AI, it's important to consider the ethical implications, including privacy concerns, potential job displacement, and the need for transparency and accountability in AI systems.

In the next section, we'll explore the basic components of AI systems and how they work together to create intelligent behavior.`,
  hasAudio: true,
  audioUrl: 'https://example.com/audio/transcript_1.mp3',
  generatedAt: '2023-04-15T14:30:00Z',
  ttsSettings: {
    language: 'a',
    voice: 'af_bella',
    speed: 1.0
  },
  chapters: [
    { title: 'Introduction', startTime: '00:00:00' },
    { title: 'What is AI?', startTime: '00:03:45' },
    { title: 'History of AI', startTime: '00:08:30' },
    { title: 'Types of AI', startTime: '00:15:20' },
    { title: 'Applications', startTime: '00:22:15' },
    { title: 'Ethical Considerations', startTime: '00:28:40' }
  ]
};

// Mock processing result
export const mockProcessingResult = {
  id: '4',
  title: 'New AI Developments',
  status: 'processing',
  message: 'Transcript processing started'
};

// Mock audio generation result
export const mockAudioResult = {
  transcriptId: '2',
  status: 'completed',
  url: 'https://example.com/audio/transcript_2.mp3',
  message: 'Audio generation completed successfully'
};

// Mock available voices
export const mockVoices = {
  americanFemale: ['af_bella', 'af_nicole', 'af_sky', 'af_sarah'],
  americanMale: ['am_adam', 'am_michael'],
  britishFemale: ['bf_emma', 'bf_isabella'],
  britishMale: ['bm_george', 'bm_lewis']
};

// Mock audio preview
export const mockAudioPreview = {
  previewUrl: 'https://example.com/audio/preview_123.mp3',
  duration: 10 // seconds
}; 