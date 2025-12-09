import React from "react";

const badges = [
  { name: "Grammar Guru", earned: true },
  { name: "Module Master", earned: true },
  { name: "Syntax Sorcerer", earned: true },
  { name: "Vocabulary Voyager", earned: true },
  { name: "Pronunciation Pro", earned: true },
  { name: "Listening Legend", earned: true },
  { name: "Writing Wizard", earned: true },
  { name: "Speaking Star", earned: true },
  { name: "Fluency Fanatic", earned: true },
  { name: "Culture Champion", earned: true },
  { name: "Quiz Conqueror", earned: true },
  { name: "Final Exam Finisher", earned: true },
  { name: "Perfect Score Pioneer", earned: false },
  { name: "Daily Streak Keeper", earned: false },
  { name: "Peer Tutor", earned: false },
  { name: "Advanced Theorist", earned: false },
  { name: "Discussion Leader", earned: false },
  { name: "Project Submitter", earned: false }
];

export default function BadgesPage() {
  const earnedCount = badges.filter(b => b.earned).length;

  return (
    <div className="min-h-screen bg-[#07131C] text-white px-8 md:px-12 py-10">
      {/* Header */}
      <h1 className="text-4xl font-bold mb-2">My Badges</h1>
      <p className="text-gray-400 mb-10">
        You’ve collected {earnedCount} of {badges.length} badges
      </p>

      {/* Badge Grid */}
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 gap-6 max-w-6xl">
        {badges.map((badge, index) => (
          <div
            key={index}
            className={`p-6 rounded-xl flex flex-col items-center justify-center shadow-lg transition-all duration-300 ${
              badge.earned
                ? "bg-[#0D2A32] hover:shadow-cyan-500/20 hover:scale-105"
                : "bg-[#0A0F14] opacity-40"
            }`}
          >
            <div
              className={`w-16 h-16 rounded-full flex items-center justify-center mb-4 ${
                badge.earned ? "bg-cyan-600" : "bg-gray-700"
              }`}
            >
              <span className="text-2xl">🏅</span>
            </div>

            <p className="text-center text-sm font-medium">{badge.name}</p>
          </div>
        ))}
      </div>

      {/* Footer */}
      <footer className="mt-20 text-gray-500 text-sm flex justify-center gap-10">
        <a href="#" className="hover:text-white transition">About Us</a>
        <a href="#" className="hover:text-white transition">Contact</a>
        <a href="#" className="hover:text-white transition">Privacy Policy</a>
        <a href="#" className="hover:text-white transition">Terms of Service</a>
      </footer>
    </div>
  );
}
