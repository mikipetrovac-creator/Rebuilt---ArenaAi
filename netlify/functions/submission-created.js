const RESEND_API_KEY = process.env.RESEND_API_KEY;

exports.handler = async (event) => {
  // Netlify pokreće ovu funkciju za svaku uspešnu formu
  const payload = JSON.parse(event.body).payload;
  const data = payload.data; // Ovde su svi podaci iz forme

  // Tvoja email adresa na koju želiš da stižu rezervacije
  const toEmail = "info@myvalanyatravel.com"; 

  // Generisanje zbijenih redova za HTML tabelu (preskače prazna polja)
  let tableRows = "";
  const fields = [
    { label: "Tour/Package", key: "tour" },
    { label: "Client Name", key: "name" },
    { label: "Phone", key: "phone" },
    { label: "Date", key: "date" },
    { label: "Pickup Location", key: "pickup" },
    { label: "Hotel", key: "hotel" },
    { label: "Adults", key: "adults" },
    { label: "Children", key: "children" },
    { label: "Infants", key: "infants" },
    { label: "Total Price", key: "total" },
    { label: "Notes", key: "notes" },
    { label: "Language", key: "lang" },
    { label: "Client Email", key: "email" }
  ];

  fields.forEach(field => {
    if (data[field.key]) {
      tableRows += `
        <tr>
          <td style="padding: 6px 10px; border: 1px solid #dddddd; font-weight: bold; background-color: #f9f9f9; width: 35%;">${field.label}:</td>
          <td style="padding: 6px 10px; border: 1px solid #dddddd;">${data[field.key]}</td>
        </tr>
      `;
    }
  });

  // Kompletan HTML izgled mejla - čist, zbijen i profesionalan
  const emailHtml = `
    <html>
      <body style="font-family: Arial, sans-serif; color: #333; line-height: 1.4; padding: 20px;">
        <h2 style="color: #8b0000; margin-bottom: 15px; border-bottom: 2px solid #8b0000; padding-bottom: 5px;">Nova rezervacija sa sajta 🌍</h2>
        <table style="width: 100%; max-width: 600px; border-collapse: collapse; margin-bottom: 20px;">
          ${tableRows}
        </table>
        <p style="font-size: 11px; color: #777;">Ovaj imejl je automatski generisan putem Netlify funkcije.</p>
      </body>
    </html>
  `;

  // Slanje zahteva ka Resend API-ju koristeći ugrađeni fetch u Node.js
  try {
    const response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${RESEND_API_KEY}`
      },
      body: JSON.stringify({
        from: "M.Y.V. Booking <system@myvalanyatravel.com>",
        to: [toEmail],
        subject: `Nova rezervacija: ${data.tour || 'Novi izlet'} - ${data.name || ''}`,
        html: emailHtml
      })
    });

    if (response.ok) {
      return { statusCode: 200, body: "Email sent successfully" };
    } else {
      const errorText = await response.text();
      console.error("Resend API greška:", errorText);
      return { statusCode: 500, body: errorText };
    }
  } catch (error) {
    console.error("Greška u funkciji:", error);
    return { statusCode: 500, body: error.toString() };
  }
};
