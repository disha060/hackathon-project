import React from "react";

const LeaderboardPage = () => {
  const topThree = [
    {
      rank: 1,
      name: "Elara Vance",
      xp: "98,500",
      streak: 120,
      img: "https://i.pravatar.cc/100?img=1",
    },
    {
      rank: 2,
      name: "Jax Orion",
      xp: "95,200",
      streak: 115,
      img: "https://i.pravatar.cc/100?img=2",
    },
    {
      rank: 3,
      name: "Lyra Nova",
      xp: "92,800",
      streak: 112,
      img: "https://i.pravatar.cc/100?img=3",
    },
  ];

  const others = [
    { rank: 4, name: "Zane Cygnus", xp: "89,100", streak: 105 },
    { rank: 5, name: "Cora Nebula", xp: "85,600", streak: 98 },
    { rank: 6, name: "Orion Pax", xp: "82,300", streak: 95 },
    { rank: 7, name: "Seraphina Altair", xp: "79,900", streak: 91 },
    { rank: 8, name: "Kaelen Draco", xp: "77,400", streak: 88 },
    { rank: 9, name: "Rhea Vega", xp: "75,100", streak: 86 },
    { rank: 10, name: "Titus Rigel", xp: "72,800", streak: 82 },
  ];

  return (
    <div className="min-h-screen bg-[#041024] text-white px-10 py-10 font-sans">
      <header className="flex justify-between items-center mb-10">
        <h1 className="text-3xl font-bold">AMEP Leaderboard</h1>
        <button className="px-5 py-2 bg-red-400 text-black rounded-xl font-semibold hover:bg-red-300 transition">
          Log Out
        </button>
      </header>

      <div className="flex gap-4 mb-8">
        {["All-Time", "This Week", "My Class", "Pronunciation"].map(
          (tab, i) => (
            <button
              key={i}
              className={`px-5 py-2 rounded-full text-sm font-semibold transition ${
                i === 0
                  ? "bg-[#14ffc3] text-black"
                  : "bg-[#0d1b3a] text-gray-300 hover:bg-[#12254f]"
              }`}
            >
              {tab}
            </button>
          )
        )}
      </div>

      <div className="w-full max-w-5xl mx-auto">
        <table className="w-full text-left">
          <thead>
            <tr className="text-gray-400 text-sm">
              <th className="pb-4">Rank</th>
              <th className="pb-4">Learner</th>
              <th className="pb-4">XP</th>
              <th className="pb-4">Streak</th>
            </tr>
          </thead>

          <tbody className="text-base">
            {topThree.map((item) => (
              <tr
                key={item.rank}
                className="bg-[#08203A] rounded-xl overflow-hidden mb-3 flex items-center justify-between px-6 py-4 border border-[#14ffc3]/40 shadow-[0_0_15px_#14ffc3] my-3"
              >
                <td className="w-10 text-[#14ffc3] font-bold text-xl">
                  {item.rank}
                </td>

                <td className="flex items-center gap-3 w-64">
                  <img
                    src={item.img}
                    className="w-10 h-10 rounded-full"
                    alt={item.name}
                  />
                  <span className="font-semibold">{item.name}</span>
                </td>

                <td className="font-bold w-32 text-right">{item.xp}</td>
                <td className="text-orange-400 font-medium w-32 text-right">
                  🔥 {item.streak} days
                </td>
              </tr>
            ))}

            {others.map((item) => (
              <tr
                key={item.rank}
                className="bg-[#0a1a32] rounded-xl mb-3 flex items-center justify-between px-6 py-3"
              >
                <td className="w-10 text-gray-400 font-semibold">
                  {item.rank}
                </td>
                <td className="w-64 font-medium text-gray-200">{item.name}</td>
                <td className="w-32 text-right">{item.xp}</td>
                <td className="w-32 text-right text-orange-400">
                  🔥 {item.streak} days
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        <div className="flex justify-center items-center gap-3 mt-8 text-gray-300">
          <button className="px-3 py-1 rounded-full hover:bg-[#123]">
            &lt;
          </button>

          {[1, 2, 3, 4, 5].map((p) => (
            <button
              key={p}
              className={`w-8 h-8 flex items-center justify-center rounded-full ${
                p === 1 ? "bg-[#14ffc3] text-black" : "hover:bg-[#123]"
              }`}
            >
              {p}
            </button>
          ))}

          <span>…</span>

          <button className="px-3 py-1 rounded-full hover:bg-[#123]">
            &gt;
          </button>
        </div>
      </div>
    </div>
  );
};

export default LeaderboardPage;
