import React, { JSX } from 'react';

import styles from './styles.module.css';

type HomePageProps = {
    name: string;
    title: string;
    tagline: string;
    descriptionLines: string[];
};

export default function HomePage({ name, title, tagline, descriptionLines }: HomePageProps): JSX.Element {
    return (
        <section className={styles.hero}>
            <img src='/img//img.jpeg' alt={`${title} Logo`} className={styles.logo} />
            <span>{name}</span>
            <span className={styles.subtitle}>{tagline}</span>

            <hr className={styles.divider} />

            <div className={styles.description}>
                {descriptionLines && descriptionLines.length > 0 &&
                    descriptionLines.map((line, index) => (
                        <p key={index}>{line}</p>
                    ))}
            </div>

        </section>
    );
}