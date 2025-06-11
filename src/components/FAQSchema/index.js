import React from 'react';

export default function FAQSchema({ mainEntity }) {
  const faqSchema = {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "@author": {
            "@type": "Person",
            "givenName": "Daniel",
            "familyName": "Gattringer",
            "jobTitle": "Data Scientist",
            "url": "https://dangattringer.github.io/",
            "sameAs": [
              "https://linkedin.com/in/daniel-gattringer06",
              "https://x.com/_dangat"
            ],
            "affiliation": {
              "@type": "Organization",
              "name": "Crayon",
              "url": "https://www.crayon.com/"
            }
    },
    mainEntity,
  };

  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      data-rh="true"
    />
  );
}
