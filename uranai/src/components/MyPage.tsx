import React, { useState } from 'react';
import { getPeople, addPerson, deletePerson } from '../utils/person';
import { getTicketCount, useTicket, replenishTickets } from '../utils/ticket';

const MyPage: React.FC = () => {
  const [people, setPeople] = useState(getPeople());
  const [tickets, setTickets] = useState(getTicketCount());

  const handleAddPerson = () => {
    const newPerson = {
      id: people.length + 1,
      nickname: '新しい人',
      name: '',
      gender: 'unknown',
      birthDate: '',
      birthTime: '',
      birthPlace: '',
    };
    addPerson(newPerson);
    setPeople(getPeople());
  };

  const handleDeletePerson = (id: number) => {
    deletePerson(id);
    setPeople(getPeople());
  };

  const handleUseTicket = () => {
    if (useTicket()) {
      setTickets(getTicketCount());
      alert('Ticket used successfully.');
    } else {
      alert('No tickets available. Please replenish.');
    }
  };

  const handleReplenishTickets = () => {
    replenishTickets(5);
    setTickets(getTicketCount());
    alert('Tickets replenished.');
  };

  return (
    <section className="page p-4">
      <div className="page-content max-w-lg mx-auto">
        <h2 className="font-serif-special text-3xl text-center mb-8">マイページ</h2>
        <div className="card p-6 mb-8">
          <h3 className="font-serif-special text-xl mb-4">チケット情報</h3>
          <div className="flex items-center justify-between">
            <p className="text-gray-300">現在のチケット枚数:</p>
            <p className="text-3xl font-bold text-yellow-300 flex items-center">
              <i data-lucide="ticket" className="w-8 h-8 mr-2"></i>
              <span id="ticket-count">{tickets}</span>
            </p>
          </div>
          <p className="text-xs text-gray-500 mt-4">パーソナル鑑定は1日1回無料です。</p>
          <button onClick={handleUseTicket} className="bg-blue-500 hover:bg-blue-400 text-white font-bold py-2 px-4 rounded-full mt-4">
            Use Ticket
          </button>
          <button onClick={handleReplenishTickets} className="bg-green-500 hover:bg-green-400 text-white font-bold py-2 px-4 rounded-full mt-4">
            Replenish Tickets
          </button>
        </div>
        <div className="card p-6">
          <div className="flex justify-between items-center mb-4">
            <h3 className="font-serif-special text-xl">人物情報管理</h3>
            <button onClick={handleAddPerson} className="bg-purple-600 hover:bg-purple-500 text-white p-2 rounded-full">
              <i data-lucide="plus" className="w-5 h-5"></i>
            </button>
          </div>
          <p className="text-sm text-gray-400 mb-4">登録人数: <span id="person-count-info">{people.length} / 3</span></p>
          <div id="mypage-person-list" className="space-y-3">
            {people.map((person) => (
              <div key={person.id} className="bg-black bg-opacity-20 p-3 rounded-lg flex items-center justify-between">
                <p>{person.nickname}</p>
                <div>
                  <button className="text-gray-400 hover:text-white p-1">
                    <i data-lucide="edit" className="w-4 h-4"></i>
                  </button>
                  <button onClick={() => handleDeletePerson(person.id)} className="text-gray-400 hover:text-red-500 p-1">
                    <i data-lucide="trash-2" className="w-4 h-4"></i>
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div id="premium-banner" className="mt-8">
          <div className="card p-6 border-2 border-yellow-500 border-dashed">
            <h3 className="font-serif-special text-xl mb-2 text-yellow-300">プレミアムプラン</h3>
            <p className="text-gray-400 mb-4">全ての機能を<br />無制限に利用できます。</p>
            <button data-action="show-premium-modal" className="w-full bg-yellow-500 hover:bg-yellow-400 text-black font-bold py-3 rounded-full transition">
              詳しく見る
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default MyPage;
