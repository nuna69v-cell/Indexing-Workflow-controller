import React, { useEffect, useState, ReactNode } from 'react';
import { StreamChat } from 'stream-chat';
import { Chat } from 'stream-chat-react';
import 'stream-chat-react/dist/css/v2/index.css';

// The Stream Chat client should be instantiated outside the component
// to avoid recreating it on every render, unless apiKey changes.
let chatClient: StreamChat | null = null;

interface StreamProviderProps {
  apiKey: string;
  userId: string;
  userName?: string;
  userToken: string;
  children: ReactNode;
}

const StreamProvider: React.FC<StreamProviderProps> = ({
  apiKey,
  userId,
  userName = 'Trader',
  userToken,
  children
}) => {
  const [clientReady, setClientReady] = useState(false);

  useEffect(() => {
    if (!apiKey || !userId || !userToken) return;

    const setupClient = async () => {
      try {
        if (!chatClient) {
          chatClient = StreamChat.getInstance(apiKey);
        }

        // Connect user
        await chatClient.connectUser(
          {
            id: userId,
            name: userName,
          },
          userToken
        );

        setClientReady(true);
      } catch (error) {
        console.error('Failed to connect to Stream Chat:', error);
      }
    };

    setupClient();

    // Cleanup when component unmounts
    return () => {
      if (chatClient) {
        chatClient.disconnectUser().then(() => {
          console.log('Stream user disconnected');
        });
        setClientReady(false);
      }
    };
  }, [apiKey, userId, userName, userToken]);

  if (!clientReady || !chatClient) {
    return <div className="p-4 text-center">Connecting to trading network...</div>;
  }

  return (
    <Chat client={chatClient} theme="str-chat__theme-light">
      {children}
    </Chat>
  );
};

export default StreamProvider;
