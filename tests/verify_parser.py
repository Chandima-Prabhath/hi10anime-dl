
import sys
import os
from pathlib import Path
import pprint

# Add project root to sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from app.parser import LinkParser

urls = [
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_ED01_(BD_720p)_(Neo)_(559566A6).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_04_(BD_720p)_(Subsplease)_(7D9ADF14).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_07_(BD_720p)_(Subsplease)_(9C3E3B82).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Torrents/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p).torrent?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_11_(BD_720p)_(Subsplease)_(6B7ABBD1).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_01_(BD_720p)_(Subsplease)_(EC1F4F4E).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_08_(BD_720p)_(Neo)_(C40B27CE).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_OP01_(BD_720p)_(Neo)_(2EAC2439).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_11_(BD_720p)_(Neo)_(2B319290).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Torrents/(Hi10)_Aharen_san_Hakarenai_(BD_720p).torrent?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_02_(BD_720p)_(Neo)_(A13F6EFE).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_04_(BD_720p)_(Neo)_(0A2544ED).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_12_(BD_720p)_(Subsplease)_(0D99A8AE).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_10_(BD_720p)_(Neo)_(53F741F7).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_08_(BD_720p)_(Subsplease)_(129A6817).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_03_(BD_720p)_(Subsplease)_(68843932).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_09_(BD_720p)_(Subsplease)_(C61B4783).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_05_(BD_720p)_(Neo)_(A1DB9FE8).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_01_(BD_720p)_(Neo)_(47DEB0BD).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_09_(BD_720p)_(Neo)_(A2660E18).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_03_(BD_720p)_(Neo)_(43AE1BA6).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_05_(BD_720p)_(Subsplease)_(408ECAF7).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_12_(BD_720p)_(Neo)_(EE9E3C80).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_07_(BD_720p)_(Neo)_(73093ADF).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_06_(BD_720p)_(Subsplease)_(5C3A0B48).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_10_(BD_720p)_(Subsplease)_(2A0B6097).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_02_(BD_720p)_(Subsplease)_(E3943F1D).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_720p)/(Hi10)_Aharen_san_Hakarenai_-_06_(BD_720p)_(Neo)_(1EDCF8DA).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Torrents/(Hi10)_Aharen_san_Hakarenai_(BD_1080p).torrent?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_02_(BD_1080p)_(Neo)_(38334072).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_03_(BD_1080p)_(Subsplease)_(B58E1213).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_04_(BD_1080p)_(Neo)_(5FC9671B).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_09_(BD_1080p)_(Neo)_(F2556040).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_03_(BD_1080p)_(Neo)_(650E1EE8).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_06_(BD_1080p)_(Neo)_(D64CBC52).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Torrents/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p).torrent?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_ED01_(BD_1080p)_(Neo)_(E423896B).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_04_(BD_1080p)_(Subsplease)_(20DABE66).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_02_(BD_1080p)_(Subsplease)_(78967D5C).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_07_(BD_1080p)_(Subsplease)_(E829C98E).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_09_(BD_1080p)_(Subsplease)_(4FD6CA11).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_01_(BD_1080p)_(Neo)_(0FF004E2).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_12_(BD_1080p)_(Neo)_(ACB1FB10).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_08_(BD_1080p)_(Subsplease)_(49938DA8).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_11_(BD_1080p)_(Subsplease)_(EFB5DA12).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_01_(BD_1080p)_(Subsplease)_(7776EE80).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_10_(BD_1080p)_(Subsplease)_(C206217A).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_12_(BD_1080p)_(Subsplease)_(E9B712D7).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_OP01_(BD_1080p)_(Neo)_(56EB3712).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_05_(BD_1080p)_(Neo)_(4DE55B69).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_06_(BD_1080p)_(Subsplease)_(4A817E35).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_08_(BD_1080p)_(Neo)_(2875ACC3).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_1080p)/(Hi10)_Aharen_san_wa_Hakarenai_S2_-_05_(BD_1080p)_(Subsplease)_(24D21C54).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_10_(BD_1080p)_(Neo)_(0068549F).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_07_(BD_1080p)_(Neo)_(EE2FA65B).mkv?jtoken=17d26554d7",
"https://f005.backblazeb2.com/file/noro-27be5839/Shows/(Hi10)_Aharen_san_Hakarenai_(BD_1080p)/(Hi10)_Aharen_san_Hakarenai_-_11_(BD_1080p)_(Neo)_(B21641C6).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_01_(BD_720p)_(jsum)_(4083357B).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_01_(BD_1080p)_(jsum)_(C674E528).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_02_(BD_720p)_(jsum)_(9D698EB8).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_02_(BD_1080p)_(jsum)_(AF6AD76F).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_03_(BD_720p)_(jsum)_(A0AABEF4).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_03_(BD_1080p)_(jsum)_(901BB40B).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_04_(BD_1080p)_(jsum)_(33B66ACB).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_04_(BD_720p)_(jsum)_(F0703BDE).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_05_(BD_720p)_(jsum)_(4C7744EB).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_05_(BD_1080p)_(jsum)_(B69126E0).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_06_(BD_1080p)_(jsum)_(3AA186D2).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_06_(BD_720p)_(jsum)_(A620A026).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_07_(BD_1080p)_(jsum)_(9494A7DA).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_07_(BD_720p)_(jsum)_(C93B6512).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_08_(BD_1080p)_(jsum)_(D08721F0).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_08_(BD_720p)_(jsum)_(187D906D).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_09_(BD_1080p)_(jsum)_(61655178).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_09_(BD_720p)_(jsum)_(EFEBD02D).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_10_(BD_1080p)_(jsum)_(347674D2).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_10_(BD_720p)_(jsum)_(ECCAE6C0).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_11_(BD_720p)_(jsum)_(44EBC423).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_11_(BD_1080p)_(jsum)_(96761A3A).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_12_(BD_720p)_(jsum)_(80ACFD00).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_12_(BD_1080p)_(jsum)_(A762D06C).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_13_(BD_720p)_(jsum)_(FCC2A5DF).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_13_(BD_1080p)_(jsum)_(0F6AFA7D).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/[Hi10]_Kageki_Shoujo!!_[BD_720p].torrent?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/OperaGirl!DualAudioPatch720p.7z?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/[Hi10]_Kageki_Shoujo!!_[BD_1080p].torrent?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/OperaGirl!DualAudioPatch1080p.7z?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_NCED1_(BD_720p)_(jsum)_(67CC5CF2).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_NCED1_(BD_1080p)_(jsum)_(60B29993).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_NCED2_(BD_720p)_(jsum)_(F35DB47E).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_NCED2_(BD_1080p)_(jsum)_(B8F285F9).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_NCED3_(BD_720p)_(jsum)_(EA6BCD9C).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_NCED3_(BD_1080p)_(jsum)_(AB502C6C).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_NCED4_(BD_1080p)_(jsum)_(1607A8A4).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_NCED4_(BD_720p)_(jsum)_(1F87CBBB).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_NCED5_(BD_720p)_(jsum)_(E99B5BAD).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_NCED5_(BD_1080p)_(jsum)_(D27FD92A).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_1080p]/(Hi10)_Kageki_Shoujo!!_-_NCOP_(BD_1080p)_(jsum)_(4E938A4D).mkv?jtoken=17d26554d7",
"https://sinbad.hi10anime.com/krome/[Hi10]_Kageki_Shoujo!!_[BD_720p]/(Hi10)_Kageki_Shoujo!!_-_NCOP_(BD_720p)_(jsum)_(E7C032A2).mkv?jtoken=17d26554d7"
]

results = LinkParser.parse(set(urls))

# Sort keys for consistent output
sorted_seasons = sorted(results.keys())


with open('tests/verify_output.txt', 'w', encoding='utf-8') as f:
    for season in sorted_seasons:
        f.write(f"Season: {season}\n")
        qualities = results[season]
        sorted_qualities = sorted(qualities.keys())
        for quality in sorted_qualities:
            f.write(f"  Quality: {quality}\n")
            episodes = qualities[quality]
            for ep in episodes:
                f.write(f"    Episode: {ep['episode']} | Type: {ep['file_type']} | File: {ep['filename']}\n")

