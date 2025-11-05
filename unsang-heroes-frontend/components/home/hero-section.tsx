import { MapPin, Quote } from "lucide-react";

export function HeroSection({ story }) {
  return (
    <section className="pt-20 pb-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-6xl mx-auto">
        <div className="text-center mb-16">
          <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-[#2c3e50] leading-tight font-[Merriweather] mb-6">
            Every Neighborhood Has Heroes
          </h1>
          <p className="text-lg text-[#7f8c8d] max-w-2xl mx-auto leading-relaxed">
            Real stories from real people doing extraordinary things in
            ordinary moments. These are your neighbors, your coworkers, the
            quiet ones changing everything.
          </p>
        </div>

        <div className="bg-white rounded-3xl shadow-lg overflow-hidden mb-12 border border-[#f4d03f]/30">
          <div className="md:flex">
            <div className="md:w-2/5">
              <img
                src={story.image}
                alt={story.name}
                className="w-full h-64 md:h-full object-cover"
              />
            </div>
            <div className="p-8 md:p-12 md:w-3/5">
              <div className="flex items-center text-[#e67e22] text-sm font-medium mb-4">
                <MapPin className="w-4 h-4 mr-2" />
                {story.location}
              </div>
              <h2 className="text-2xl font-bold text-[#2c3e50] mb-4 font-[Merriweather]">
                Meet {story.name}
              </h2>
              <Quote className="w-8 h-8 text-[#f4d03f] mb-4" />
              <p className="text-[#7f8c8d] leading-relaxed mb-6 text-lg italic">
                "{story.quote}"
              </p>
              <p className="text-[#2c3e50] leading-relaxed mb-6">
                {story.story}
              </p>
              <div className="flex items-center justify-between">
                <div className="bg-[#f4d03f]/20 px-4 py-2 rounded-full">
                  <span className="text-[#e67e22] font-semibold text-sm">
                    {story.impact}
                  </span>
                </div>
                <button className="text-[#e67e22] font-medium hover:text-[#d35400] transition-colors">
                  Read Full Story →
                </button>
              </div>
            </div>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center mb-16">
          <button className="px-8 py-4 bg-[#e67e22] text-white font-medium rounded-full hover:bg-[#d35400] transition-all duration-200 hover:scale-105 active:scale-95 shadow-lg">
            Nominate Someone You Know
          </button>
          <button className="px-8 py-4 border-2 border-[#e67e22] text-[#e67e22] font-medium rounded-full hover:bg-[#e67e22] hover:text-white transition-all duration-200 hover:scale-105 active:scale-95">
            Browse All Stories
          </button>
        </div>
      </div>
    </section>
  );
}
