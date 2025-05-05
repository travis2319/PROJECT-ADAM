// components/chat/ResponseViewer.tsx
import React from 'react';
import { ScrollView } from 'react-native';
import Markdown from 'react-native-markdown-display';

interface ResponseViewerProps {
  response: string;
}

const ResponseViewer: React.FC<ResponseViewerProps> = ({ response }) => {
  return (
    <ScrollView className="mt-4">
      <Markdown>{response}</Markdown>
    </ScrollView>
  );
};

export default ResponseViewer;