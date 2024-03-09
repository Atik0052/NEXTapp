
import { NextApiRequest, NextApiResponse } from 'next';
import qrcode from 'qrcode';

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  console.log('Received Request:', req.method);

  try {
    if (req.method === 'GET') {
      const { phoneNumber, message } = req.query;
      console.log('Received Data:', { phoneNumber, message });

      const link = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
      const qrCodeDataURL = await qrcode.toDataURL(link);
      return res.json({ link, qrCodeDataURL });
    } 
      
    else if (req.method === 'POST') {
      const { phoneNumber, message } = req.body;
      console.log('Received Data:', { phoneNumber, message });

      const link = `https://wa.me/${phoneNumber}?text=${encodeURIComponent(message)}`;
      const qrCodeDataURL = await qrcode.toDataURL(link);
      return res.json({ link, qrCodeDataURL });
    } else {
      // If the method is not GET or POST, return a 405 Method Not Allowed response
      return res.status(405).json({ error: 'Method Not Allowed' });
    }
  } catch (error) {
    console.error('Error in generateQRCode:', error);
    return res.status(500).json({ error: 'Internal Server Error' });
  }
}

