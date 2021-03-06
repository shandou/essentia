#!/usr/bin/env python

# Copyright (C) 2006-2020  Music Technology Group - Universitat Pompeu Fabra
#
# This file is part of Essentia
#
# Essentia is free software: you can redistribute it and/or modify it under
# the terms of the GNU Affero General Public License as published by the Free
# Software Foundation (FSF), either version 3 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
# details.
#
# You should have received a copy of the Affero GNU General Public License
# version 3 along with this program. If not, see http://www.gnu.org/licenses/



from essentia import *
from essentia.standard import *

def extractor(filename):
    # load our audio into an array
    audio = MonoLoader(filename=filename, sampleRate=44100)()

    # create the pool and the necessary algorithms
    pool = Pool()
    w = Windowing()
    spec = Spectrum()
    centroid = Centroid(range=22050)

    # compute the centroid for all frames in our audio and add it to the pool
    for frame in FrameGenerator(audio, frameSize = 1024, hopSize = 512):
        c = centroid(spec(w(frame)))
        pool.add('lowlevel.centroid', c)

    # aggregate the results
    aggrpool = PoolAggregator(defaultStats = [ 'mean', 'stdev' ])(pool)

    # write result to file
    YamlOutput(filename = filename+'.features.yaml')(aggrpool)


# some python magic so that this file works as a script as well as a module
# if you do not understand what that means, you don't need to care
if __name__ == '__main__':
    import sys

    try:
        input_file = sys.argv[1]
    except:
        print("usage: %s <input_file>" % sys.argv[0])
        sys.exit()

    extractor(sys.argv[1])
    print('Results written to %s' % input_file+'.features.yaml')
