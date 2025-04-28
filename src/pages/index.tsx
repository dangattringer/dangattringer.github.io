import React, { JSX } from 'react';
import Layout from '@theme/Layout';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

import HomePage from '../components/Home';

function Home(): JSX.Element {
  const { siteConfig } = useDocusaurusContext();
  const descriptionLines = siteConfig.customFields.descriptionLines as string[] || [];

  return (
    <Layout
      title={`Home - ${siteConfig.title}`}
      description={siteConfig.customFields?.description as string || siteConfig.tagline}
    >
      <main>
        <HomePage
          name={siteConfig.customFields.name as string}
          title={siteConfig.title}
          tagline={siteConfig.tagline}
          descriptionLines={descriptionLines}
        />
      </main>
    </Layout>
  );
}

export default Home;