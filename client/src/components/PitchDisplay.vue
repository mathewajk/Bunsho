<script setup lang="ts">

const props = defineProps<{
    word: {
        word: string,
        reading: string,
        pitch: number,
    },
}>()

const getMorae = ( word:string ) => {
  let chars = word.split('');
  let morae = [];
  let currentMora = chars.shift();

  for(let i in chars) {
      if(['ゃ','ゅ','ょ'].includes(chars[i])) {
          currentMora += chars[i];
      } else {
          morae.push(currentMora);
          currentMora = chars[i];
      }
  }
  morae.push(currentMora);
  return morae;
}

const getPitch = () => {
    return getMorae( props.word.reading ).map( (mora, i) => {
        
        let height = "low";
        
        /* The first mora can only be either peak pitch (pitch = 1) or low pitch.
           Subsequent morae are high until the peak is encountered, then low.
           If there is no peak (pitch = 0), all subsequent morae are high.
           Sequences like しゃ, しゅ, しょ are considered one mora.
        */

        if(i == 0) { 
          height = ( props.word.pitch == 1 ? "peak" : "start" );
        } else {
          if (props.word.pitch == 0 || i < props.word.pitch - 1)
            height = "high"
          else if (i == props.word.pitch - 1)
            height = "peak"
        }

        let key = i + '_' + mora;
        let numChars = mora?.split('').length;

        return {
            mora: mora,
            key: key,
            height: height,
            numChars: numChars,
        }
    });
}
</script>

<template>

<div class="pitchDisplay">
    <span v-for="mora, i in getPitch()" 
        class="mora"
        :key="i"
        :data-pitch="mora.height"
        :data-characters="mora.numChars">{{mora.mora}}</span>
    <span class="sr-only"> - Pitch accent: {{ word.pitch }}</span>
</div>
</template>

<style scoped>
.mora {
    position: relative;
    margin: 0.1em;
  }
  
.pitchDisplay {
    position: relative;
    display: block;
    margin-bottom: 1em;
}

.mora::before, .mora::after {
    content: "";
    position: absolute;
    top: -0.1em;
}

.mora::before {
    height: 0.2em;
    left: -0.2em;
    width: 1.2em;
}

.mora[data-pitch="low"]::before, .mora[data-pitch="start"]::before {
    height: 0.2em;
    left: -0.2em;
    width: 1.4em;
    top: 1.5em;
    background-color: #330D00;
}

.mora[data-pitch="start"]::after {
    height: 1.75em;
    width: 0.2em;
    right: -0.2em;
    background-color: #330D00;
}

.mora[data-characters="2"]::before {
    height: 0.2em;
    width: 2.4em;
}

.mora[data-pitch="high"]::before {
    background-color: #330D00;
}

.mora[data-pitch="peak"]::before, .mora[data-pitch="peak"]::after {
    background-color: orangered;
}
  
.mora[data-pitch="peak"]::after {
    height: 1.75em;
    width: 0.2em;
    left: 1em;
}

.mora[data-pitch="peak"][data-characters="2"]::after {
    left: 2em;
}

.mora[data-pitch="peak"] {
    color: orangered;
}
  
.sr-only {
    position: absolute;
    width: 1px;
    height: 1px;
    padding: 0;
    overflow: hidden;
    clip: rect(0, 0, 0, 0);
    word-wrap: normal;
    border: 0;
}

</style>