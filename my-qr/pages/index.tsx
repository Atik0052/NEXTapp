
import React, { useState } from 'react';
import QRCode from 'qrcode.react';

const Home: React.FC = () => {
  const [selectedCountry, setSelectedCountry] = useState<string>('+1');
  const [phoneNumber, setPhoneNumber] = useState<string>('');
  const [message, setMessage] = useState<string>('');
  const [qrCodeValue, setQRCodeValue] = useState<string | null>(null);
  const [linkValue, setLinkValue] = useState<string | null>(null);

  const countryCodes = [
    { label: '+1 (US)', value: '+1' },
    { label: '+44 (UK)', value: '+44' },
    { label: '+33 (France)', value: '+33' },
    { label: '+49 (Germany)', value: '+49' },
    { label: '+81 (Japan)', value: '+81' },
    { label: '+86 (China)', value: '+86' },
    { label: '+91 (India)', value: '+91' },
    { label: '+61 (Australia)', value: '+61' },
    { label: '+7 (Russia)', value: '+7' },
    { label: '+27 (South Africa)', value: '+27' }
    ];

  const generateQRCode = async () => {
    if (!phoneNumber || !message) {
      alert('Enter phone number and message to proceed.');
      return;
    }

    const fullPhoneNumber = `${selectedCountry}${phoneNumber}`;

    try {
      const response = await fetch('/api/qr-generate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          phoneNumber: fullPhoneNumber,
          message,
        }),
      });

      if (!response.ok) {
        console.error('Failed to generate QR code:', response.status, response.statusText);
        throw new Error('Failed to generate QR code');
      }

      const result = await response.json();
      console.log('API Response:', result);

      setQRCodeValue(result.link);
      setLinkValue(result.link);
    } catch (error) {
      console.error('Error:', message);
    }
  };

  return (
    <div style={{ backgroundColor: '#f0f0f0', padding: '50px' }}>
      <h1>Whatsapp QR Code Generator</h1>
      <br />
      <h3>Enter Phone number and Message</h3>
      <label>
        Country Code:
        <select
          value={selectedCountry}
          onChange={(e) => setSelectedCountry(e.target.value)}
          aria-label="Country Code"
        >
          {countryCodes.map((code) => (
            <option key={code.value} value={code.value}>
              {code.label}
            </option>
          ))}
        </select>
        <input
          type="tel"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          aria-label="Phone Number"
        />
      </label>
      <label>
        Message:
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          aria-label="Message"
        />
      </label>
      <button onClick={generateQRCode}>Generate QR Code</button>

      {qrCodeValue && (
        <>
          <p>Generated Link: {linkValue}</p>
          <QRCode value={qrCodeValue} size={128} />
        </>
      )}
    </div>
  );
};

export default Home;








