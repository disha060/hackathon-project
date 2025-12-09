import React from "react";
import { Card, CardContent } from "../ui/card";
import { Search, User } from "lucide-react";

export default function DashboardUI() {
  return (
    <div className="min-h-screen bg-[#0F172A] text-white flex">
      {/* Sidebar */}
      <aside className="w-60 bg-[#0B1120] p-6 flex flex-col gap-6">
        <h1 className="text-2xl font-bold">AMEP</h1>
        <nav className="flex flex-col gap-4 text-gray-300">
          <a className="hover:text-white" href="#">Dashboard</a>
          <a className="hover:text-white" href="#">Courses</a>
          <a className="hover:text-white" href="#">Messages</a>
          <a className="hover:text-white" href="#">Achievements</a>
        </nav>
        <div className="mt-auto text-gray-400 flex flex-col gap-3">
          <button className="hover:text-white">Settings</button>
          <button className="hover:text-white">Logout</button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <h2 className="text-3xl font-semibold">Dashboard</h2>
          <div className="flex items-center gap-4">
            <div className="flex bg-[#1E293B] px-3 py-2 rounded-xl items-center">
              <Search className="w-4 h-4 text-gray-300" />
              <input
                className="bg-transparent outline-none ml-2 text-sm"
                placeholder="Search..."
              />
            </div>
            <div className="w-10 h-10 bg-gray-600 rounded-full flex items-center justify-center">
              <User />
            </div>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-3 gap-6 mb-8">
          <Card className="bg-gradient-to-br from-blue-700 to-cyan-500 text-white">
            <CardContent className="p-6">
              <p>Total XP</p>
              <h1 className="text-3xl font-bold">12,500</h1>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-orange-500 to-pink-500 text-white">
            <CardContent className="p-6">
              <p>Learning Streak</p>
              <h1 className="text-3xl font-bold">12 Days</h1>
            </CardContent>
          </Card>

          <Card className="bg-gradient-to-br from-purple-600 to-indigo-500 text-white">
            <CardContent className="p-6">
              <p>Your Level</p>
              <h1 className="text-3xl font-bold">Level 5</h1>
            </CardContent>
          </Card>
        </div>

        {/* Weekly Activity + Course Completion */}
        <div className="grid grid-cols-3 gap-6 mb-10">
          <Card className="col-span-2 bg-[#1E293B]">
            <CardContent className="p-6">
              <h3 className="text-xl mb-4">Weekly Activity</h3>
              <div className="w-full h-40 bg-[#0F172A] rounded-xl" />
            </CardContent>
          </Card>

          <Card className="bg-[#1E293B]">
            <CardContent className="p-6">
              <h3 className="text-xl mb-4">Course Completion</h3>
              <div className="space-y-4">
                <Progress label="Advanced" value={80} />
                <Progress label="Conversational Skills" value={60} />
                <Progress label="Business English" value={45} />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Continue Learning */}
        <h3 className="text-xl mb-4">Continue Learning</h3>
        <div className="grid grid-cols-3 gap-6">
          {learningCards.map((card) => (
            <Card key={card.title} className="bg-[#1E293B]">
              <CardContent className="p-4">
                <img src={card.img} className="rounded-xl mb-3" />
                <h4 className="font-semibold mb-1">{card.title}</h4>
                <p className="text-gray-400 text-sm mb-3">{card.desc}</p>
                <button className="text-blue-400 text-sm">Continue →</button>
              </CardContent>
            </Card>
          ))}
        </div>
      </main>
    </div>
  );
}

function Progress({ label, value }) {
  return (
    <div>
      <p className="text-sm mb-1">{label}</p>
      <div className="w-full h-2 bg-gray-700 rounded-full">
        <div
          className="h-full bg-blue-500 rounded-full"
          style={{ width: `${value}%` }}
        ></div>
      </div>
    </div>
  );
}

const learningCards = [
  {
    title: "Advanced Conversational Skills",
    desc: "Improve fluency and confidence.",
    img: "https://via.placeholder.com/300x150",
  },
  {
    title: "Writing for Business",
    desc: "Craft professional communication.",
    img: "https://via.placeholder.com/300x150",
  },
  {
    title: "Public Speaking Mastery",
    desc: "Boost your presentation skills.",
    img: "https://via.placeholder.com/300x150",
  },
];
