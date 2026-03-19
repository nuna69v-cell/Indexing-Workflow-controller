import React, { useEffect, useState } from 'react';
import {
  Channel,
  ChannelHeader,
  MessageInput,
  MessageList,
  Thread,
  Window,
  ChannelList
} from 'stream-chat-react';
import { useChatContext } from 'stream-chat-react';
import type { Channel as StreamChannel } from 'stream-chat';

export const TradingChat: React.FC = () => {
  const { client } = useChatContext();
  const [activeChannel, setActiveChannel] = useState<StreamChannel | null>(null);

  // Filtering logic: e.g. show all 'trading' channels
  const filters = { type: 'messaging' };
  const sort = { last_message_at: -1 } as const;

  // Optionally, you could dynamically create a 'Global Trading Room' channel
  // if it doesn't exist yet, but typically that is done server-side.
  useEffect(() => {
    const initDefaultChannel = async () => {
      try {
        const globalChannel = client.channel('messaging', 'global-trading-room', {
          name: "Global Trading Room" as any,
        });
        await globalChannel.watch();
        setActiveChannel(globalChannel);
      } catch (e) {
        console.error("Error setting default channel", e);
      }
    };
    if (client) {
      initDefaultChannel();
    }
  }, [client]);

  return (
    <div className="flex h-[600px] border border-gray-200 rounded-lg overflow-hidden bg-white shadow-lg">
      <div className="w-1/3 min-w-[250px] border-r border-gray-200 hidden md:block">
        <ChannelList
          filters={filters}
          sort={sort}
        />
      </div>
      <div className="w-full md:w-2/3">
        {activeChannel ? (
          <Channel channel={activeChannel}>
            <Window>
              <ChannelHeader />
              <MessageList />
              <MessageInput />
            </Window>
            <Thread />
          </Channel>
        ) : (
          <div className="flex h-full items-center justify-center text-gray-500">
            Joining global trading room...
          </div>
        )}
      </div>
    </div>
  );
};

export default TradingChat;
