/// <reference types="vite/client" />

declare module 'vue-timeago3';

type Word = {
    id: number,
    pos: number,
    text: string,
    gloss: string,
    seen: boolean,
    last_seen: string,
    due: string,
    interval: number,
    easing_factor: number
}

type Sentence = {
    id: number,
    text: string,
    created_at: string,
    seen: boolean,
    due: string,
    words: Word[]
}

type Question = {
    sentence: Sentence | null,
    target: Word | null
}