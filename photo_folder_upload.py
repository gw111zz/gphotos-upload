#!/usr/bin/perl -lw

use strict;

use Data::Dumper;
use File::Find;

if (! $ARGV[0]) {
  die <<EOF
  This script generates Python3 commands to upload photos organized in folders to Google Photos.
  It searches the provided directory recursively uploads the photo into an album with the same 
  name as the containing folder.

  e.g. If there are photos stored in the following folder structure:

  family/baby/photo1.jpg
  family/holiday/photo2.jpg

  then two albums "baby" and "holiday" will be created and photo1.jpg will be in the album "baby"
  and photo2.jpg will be in the album "holiday".

  Usage: $0 <path to folder containing photos>
EOF
  ;
}

my $dir = $ARGV[0];
print "$dir\n";
my @files = glob_files($dir);

sub glob_files {
    my ($dir) = @_;
    my @files;
    find(sub { push @files, $File::Find::name if -f }, $dir);
    return @files
}

# Key = album name, Value = array of paths to photos in the album
my %albums;

for (@files) {
  my @path_components = split(/\//);
  my $size = @path_components;
  # Push the filename into the array in the albums hash at key "album name"
  # thereby sorting the photos by album.
  my $current_album = $path_components[$size - 2];
  my $full_path_to_photo = $_; 
  push @{$albums{$current_album}}, $full_path_to_photo; 
}

while ((my $current_album, my $photos) = each (%albums)) {
  print "python3 ./upload.py --auth auth.txt --album \"$current_album\" " . join' ', map qq("$_"), @$photos;
}

