"use client";

import React, { useEffect, useRef, useState } from 'react';
import maplibregl from 'maplibre-gl';
import 'maplibre-gl/dist/maplibre-gl.css';

interface MapProps {
  center?: [number, number];
  zoom?: number;
}

export function HyperLocalMap({ center = [78.9629, 20.5937], zoom = 5 }: MapProps) {
  const mapContainer = useRef<HTMLDivElement>(null);
  const map = useRef<maplibregl.Map | null>(null);
  
  const [layers, setLayers] = useState({
    competitors: true,
    markets: true,
    suppliers: false,
    pois: true,
    transport: false,
  });

  useEffect(() => {
    if (map.current || !mapContainer.current) return;
    
    // Initialize map using standard OSM tiles for demonstration
    map.current = new maplibregl.Map({
      container: mapContainer.current,
      style: {
        version: 8,
        sources: {
          'osm-tiles': {
            type: 'raster',
            tiles: [
              'https://tile.openstreetmap.org/{z}/{x}/{y}.png'
            ],
            tileSize: 256,
            attribution: '© OpenStreetMap contributors'
          }
        },
        layers: [{
          id: 'osm-tiles-layer',
          type: 'raster',
          source: 'osm-tiles',
          minzoom: 0,
          maxzoom: 19
        }]
      },
      center: center,
      zoom: zoom,
    });

    map.current.addControl(new maplibregl.NavigationControl(), 'top-right');
    
    // Add a mock marker for user location
    new maplibregl.Marker({ color: '#0d9488' })
      .setLngLat(center)
      .setPopup(new maplibregl.Popup().setHTML("<h4>Your Location</h4>"))
      .addTo(map.current);

  }, [center, zoom]);

  const toggleLayer = (key: keyof typeof layers) => {
    setLayers(prev => ({ ...prev, [key]: !prev[key] }));
    // In a real implementation, this would toggle visibility of geojson layers on map.current
  };

  return (
    <div className="w-full h-[500px] flex rounded-xl overflow-hidden shadow-sm border border-slate-200">
      <div className="w-64 bg-white p-4 border-r border-slate-200 flex flex-col">
        <h3 className="font-bold text-slate-800 mb-4">Map Controls</h3>
        
        <div className="space-y-3 flex-1">
          {Object.entries(layers).map(([key, active]) => (
            <label key={key} className="flex items-center space-x-3 cursor-pointer">
              <input 
                type="checkbox" 
                checked={active} 
                onChange={() => toggleLayer(key as keyof typeof layers)}
                className="w-4 h-4 text-teal-600 rounded border-slate-300 focus:ring-teal-500"
              />
              <span className="text-sm font-medium text-slate-700 capitalize">
                {key === 'pois' ? 'Relevant POIs' : key}
              </span>
            </label>
          ))}
        </div>

        <div className="mt-auto pt-4 border-t border-slate-200">
          <h4 className="text-xs font-bold text-slate-500 uppercase mb-2">Local Insights</h4>
          <div className="space-y-1 text-sm text-slate-700">
            <p>Registered businesses: <span className="font-bold">11</span></p>
            <p>Market signal: <span className="font-bold text-teal-600">Medium</span></p>
            <p>Price evidence: <span className="font-bold text-teal-600">Strong</span></p>
          </div>
          <div className="mt-3 bg-slate-100 rounded p-2 text-xs text-slate-500">
            Evidence coverage: 68%
          </div>
        </div>
      </div>
      
      <div className="flex-1 bg-slate-100 relative">
        <div ref={mapContainer} className="absolute inset-0 w-full h-full" />
      </div>
    </div>
  );
}
