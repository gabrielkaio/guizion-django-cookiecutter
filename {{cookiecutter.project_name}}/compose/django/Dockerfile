FROM python:3.6.6-alpine3.8

MAINTAINER Guizion Labs <contato@guizion.com>

ENV PYTHONUNBUFFERED 1

#RUN apk update -y && apk add binutils libproj-dev gdal-bin

#RUN apk install locales locales-all

ENV FFMPEG_VERSION=3.4.1
ENV LC_ALL pt_BR.UTF-8
ENV LANG pt_BR.UTF-8
ENV LANGUAGE pt_BR.UTF-8

RUN apk add --update py-pip build-base curl nasm tar bzip2 \
  zlib-dev yasm-dev lame-dev libogg-dev x264-dev\
   libvpx-dev libvorbis-dev x265-dev freetype-dev libass-dev \
    libwebp-dev rtmpdump-dev libtheora-dev opus-dev

#  DIR=$(mktemp -d) && cd ${DIR} && \
#
#  curl -s http://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.gz | tar zxvf - -C . && \
#  cd ffmpeg-${FFMPEG_VERSION} && \
#  ./configure \
#  --enable-version3 --enable-gpl --enable-nonfree --enable-small \
#   --enable-libmp3lame --enable-libx264 --enable-libx265 \
#    --enable-libvpx --enable-libtheora --enable-libvorbis \
#     --enable-libopus --enable-libass --enable-libwebp \
#      --enable-librtmp --enable-postproc --enable-avresample \
#       --enable-libfreetype --disable-debug && \
#  make && \
#  make install && \
#  make distclean && \
#
#  rm -rf ${DIR} && \
#  apk del curl tar bzip2 x264 nasm && rm -rf /var/cache/apk/*

RUN apk update

RUN apk add --update postgresql-dev gcc libffi-dev linux-headers jpeg-dev zlib-dev git

RUN mkdir -p /app

COPY . /app

RUN pip install --no-cache-dir -r /app/{{cookiecutter.project_name}}/config/requirements/local.txt

RUN apk add --update bash && rm -rf /var/cache/apk/*

WORKDIR /app
