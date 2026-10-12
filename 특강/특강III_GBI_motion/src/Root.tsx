import React from 'react';
import {Composition} from 'remotion';
import {M7E00, M7E00_TOTAL} from './episodes/M7E00';
import {M7E01, M7E01_TOTAL} from './episodes/M7E01';
import {M7E02, M7E02_TOTAL} from './episodes/M7E02';
import {M7E03, M7E03_TOTAL} from './episodes/M7E03';
import {M7E04, M7E04_TOTAL} from './episodes/M7E04';
import {M7E05, M7E05_TOTAL} from './episodes/M7E05';
import {M7E06, M7E06_TOTAL} from './episodes/M7E06';
import {M7E07, M7E07_TOTAL} from './episodes/M7E07';
import {M7E08, M7E08_TOTAL} from './episodes/M7E08';
import {M7E09, M7E09_TOTAL} from './episodes/M7E09';
import {M8E00, M8E00_TOTAL} from './episodes/M8E00';
import {M8E01, M8E01_TOTAL} from './episodes/M8E01';
import {M8E02, M8E02_TOTAL} from './episodes/M8E02';
import {M8E03a, M8E03a_TOTAL} from './episodes/M8E03a';
import {M8E03b, M8E03b_TOTAL} from './episodes/M8E03b';
import {M8E03c, M8E03c_TOTAL} from './episodes/M8E03c';
import {M8E04, M8E04_TOTAL} from './episodes/M8E04';
import {M8E05, M8E05_TOTAL} from './episodes/M8E05';
import {M8E06, M8E06_TOTAL} from './episodes/M8E06';
import {M8E07, M8E07_TOTAL} from './episodes/M8E07';
import {M8E08, M8E08_TOTAL} from './episodes/M8E08';
import {M8E09, M8E09_TOTAL} from './episodes/M8E09';
import {M8E10, M8E10_TOTAL} from './episodes/M8E10';

const EPS: [string, React.FC, number][] = [
  ['M7E00', M7E00, M7E00_TOTAL],
  ['M7E01', M7E01, M7E01_TOTAL],
  ['M7E02', M7E02, M7E02_TOTAL],
  ['M7E03', M7E03, M7E03_TOTAL],
  ['M7E04', M7E04, M7E04_TOTAL],
  ['M7E05', M7E05, M7E05_TOTAL],
  ['M7E06', M7E06, M7E06_TOTAL],
  ['M7E07', M7E07, M7E07_TOTAL],
  ['M7E08', M7E08, M7E08_TOTAL],
  ['M7E09', M7E09, M7E09_TOTAL],
  ['M8E00', M8E00, M8E00_TOTAL],
  ['M8E01', M8E01, M8E01_TOTAL],
  ['M8E02', M8E02, M8E02_TOTAL],
  ['M8E03a', M8E03a, M8E03a_TOTAL],
  ['M8E03b', M8E03b, M8E03b_TOTAL],
  ['M8E03c', M8E03c, M8E03c_TOTAL],
  ['M8E04', M8E04, M8E04_TOTAL],
  ['M8E05', M8E05, M8E05_TOTAL],
  ['M8E06', M8E06, M8E06_TOTAL],
  ['M8E07', M8E07, M8E07_TOTAL],
  ['M8E08', M8E08, M8E08_TOTAL],
  ['M8E09', M8E09, M8E09_TOTAL],
  ['M8E10', M8E10, M8E10_TOTAL],
];

export const RemotionRoot: React.FC = () => (
  <>
    {EPS.map(([id, C, n]) => (
      <Composition key={id} id={id} component={C} durationInFrames={n} fps={30} width={1920} height={1080} />
    ))}
  </>
);
