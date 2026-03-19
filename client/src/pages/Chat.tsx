import React, { useState, useEffect } from 'react';
import StreamProvider from '../components/StreamProvider';
import TradingChat from '../components/TradingChat';

export const ChatPage: React.FC = () => {
  const [token, setToken] = useState<string | null>(null);
  const [userId, ] = useState<string>('trader_' + Math.floor(Math.random() * 10000));
  const apiKey = import.meta.env.VITE_STREAM_API_KEY || 'your_stream_api_key_here'; // Replace or use env

  useEffect(() => {
    // In a real app, you would fetch the token from your backend, passing your auth JWT
    const fetchToken = async () => {
      try {
        const API = import.meta.env.VITE_API_URL || '';
        // Note: For this demo, assuming the backend doesn't enforce strict Okta yet or we pass a mock user
        const response = await fetch(`${API}/api/v1/stream/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            user_id: userId,
            username: `Trader ${userId}`,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          setToken(data.chat_token);
        } else {
          console.error("Failed to fetch token", await response.text());
        }
      } catch (error) {
        console.error("Error fetching Stream token", error);
      }
    };

    fetchToken();
  }, [userId]);

  if (!token) {
    return <div className="flex justify-center items-center h-64">Loading Chat Environment...</div>;
  }

  return (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Global Trading Room</h1>
      <StreamProvider
        apiKey={apiKey}
        userId={userId}
        userToken={token}
      >
        <TradingChat />
      </StreamProvider>
    </div>
  );
};

export default ChatPage;
