/*
	SHA-1
	Copyright (C) 2007 MITSUNARI Shigeo at Cybozu Labs, Inc.
	license:new BSD license
	how to use
	CybozuLabs.SHA1.calc(<ascii string>);
	CybozuLabs.SHA1.calc(<unicode(UTF16) string>, CybozuLabs.SHA1.BY_UTF16);

	ex. CybozuLabs.SHA1.calc("abc") == "a9993e364706816aba3e25717850c26c9cd0d89d";
*/
var CybozuLabs = {
	SHA1 : {
		int16toBE : function(i16) {
			i16 &= 65535;
			if (i16 < 0) i16 += 65536;
			var ret = Number(i16).toString(16);
			return new Array(5 - ret.length).join("0") + ret;
		},
		int32toBE : function(i32) {
			return this.int16toBE(i32 >>> 16) + this.int16toBE(i32 & 65535);
		},
		swap32 : function(i32) {
			return (i32 << 24) | ((i32 << 8) & 0xff0000) | ((i32 >> 8) & 0xff00) | (i32 >>> 24);
		},
		swap16 : function(i16) {
			return (i16 >> 8) | ((i16 << 8) & 0xff00);
		},
		put : function(x) {
			x |= 0;
			document.write("0x" + Number(x < 0 ? x + 4294967296 : x).toString(16) + "<br>");
		},
		update_Fx : function(buf, charSize) {
			var WL = [];
			var WH = [];
			if (charSize == 1) {
				for (var i = 0; i < 16; i++) {
					var t = buf.charCodeAt(i * 4 + 0);
					WL[i] = buf.charCodeAt(i * 4 + 3) | (buf.charCodeAt(i * 4 + 2) << 8) | (buf.charCodeAt(i * 4 + 1) << 16) | ((t & 0x7) << 24);
					WH[i] = t >>> 3;
				}
			} else {
				for (var i = 0; i < 16; i++) {
					var t = this.swap16(buf.charCodeAt(i * 2 + 0));
					WL[i] = this.swap16(buf.charCodeAt(i * 2 + 1)) | (( t & 0x7ff) << 16);
					WH[i] = t >>> 11;
				}
			}
			for (var i = 16; i < 80; i++) {
				var tL = WL[i - 3] ^ WL[i - 8] ^ WL[i - 14] ^ WL[i - 16];
				var tH = WH[i - 3] ^ WH[i - 8] ^ WH[i - 14] ^ WH[i - 16];
				WL[i] = (tH >>> 4) | ((tL << 1) & 0x7ffffff);
				WH[i] = (tL >>> 26) | ((tH << 1) & 31);
			}
			var aL = this.H_[0];
			var aH = this.H_[1];
			var bL = this.H_[2];
			var bH = this.H_[3];
			var cL = this.H_[4];
			var cH = this.H_[5];
			var dL = this.H_[6];
			var dH = this.H_[7];
			var eL = this.H_[8];
			var eH = this.H_[9];

			var t;
			for (var i = 0; i < 20; i += 5) {
				eL += ((bL & cL) | (~bL & dL)) + WL[i] + (((aL & 0x3fffff) << 5) | aH) + 0x02827999;
				eH += ((bH & cH) | (~bH & dH)) + WH[i] + (aL >>> 22) + 0x0b + (eL >>> 27);
				eL &= 0x7ffffff; eH &= 31;
				t = (bL >>> 2) | ((bH & 3) << 25); bH = (bH >>> 2) | ((bL & 3) << 3); bL = t;

				dL += ((aL & bL) | (~aL & cL)) + WL[i + 1] + (((eL & 0x3fffff) << 5) | eH) + 0x02827999;
				dH += ((aH & bH) | (~aH & cH)) + WH[i + 1] + (eL >>> 22) + 0x0b + (dL >>> 27);
				dL &= 0x7ffffff; dH &= 31;
				t = (aL >>> 2) | ((aH & 3) << 25); aH = (aH >>> 2) | ((aL & 3) << 3); aL = t;

				cL += ((eL & aL) | (~eL & bL)) + WL[i + 2] + (((dL & 0x3fffff) << 5) | dH) + 0x02827999;
				cH += ((eH & aH) | (~eH & bH)) + WH[i + 2] + (dL >>> 22) + 0x0b + (cL >>> 27);
				cL &= 0x7ffffff; cH &= 31;
				t = (eL >>> 2) | ((eH & 3) << 25); eH = (eH >>> 2) | ((eL & 3) << 3); eL = t;

				bL += ((dL & eL) | (~dL & aL)) + WL[i + 3] + (((cL & 0x3fffff) << 5) | cH) + 0x02827999;
				bH += ((dH & eH) | (~dH & aH)) + WH[i + 3] + (cL >>> 22) + 0x0b + (bL >>> 27);
				bL &= 0x7ffffff; bH &= 31;
				t = (dL >>> 2) | ((dH & 3) << 25); dH = (dH >>> 2) | ((dL & 3) << 3); dL = t;

				aL += ((cL & dL) | (~cL & eL)) + WL[i + 4] + (((bL & 0x3fffff) << 5) | bH) + 0x02827999;
				aH += ((cH & dH) | (~cH & eH)) + WH[i + 4] + (bL >>> 22) + 0x0b + (aL >>> 27);
				aL &= 0x7ffffff; aH &= 31;
				t = (cL >>> 2) | ((cH & 3) << 25); cH = (cH >>> 2) | ((cL & 3) << 3); cL = t;
			}
			for (var i = 20; i < 40; i += 5) {
				eL += (bL ^ cL ^ dL) + WL[i] + (((aL & 0x3fffff) << 5) | aH) + 0x06d9eba1;
				eH += (bH ^ cH ^ dH) + WH[i] + (aL >>> 22) + 0x0d + (eL >>> 27);
				eL &= 0x7ffffff; eH &= 31;
				t = (bL >>> 2) | ((bH & 3) << 25); bH = (bH >>> 2) | ((bL & 3) << 3); bL = t;

				dL += (aL ^ bL ^ cL) + WL[i + 1] + (((eL & 0x3fffff) << 5) | eH) + 0x06d9eba1;
				dH += (aH ^ bH ^ cH) + WH[i + 1] + (eL >>> 22) + 0x0d + (dL >>> 27);
				dL &= 0x7ffffff; dH &= 31;
				t = (aL >>> 2) | ((aH & 3) << 25); aH = (aH >>> 2) | ((aL & 3) << 3); aL = t;

				cL += (eL ^ aL ^ bL) + WL[i + 2] + (((dL & 0x3fffff) << 5) | dH) + 0x06d9eba1;
				cH += (eH ^ aH ^ bH) + WH[i + 2] + (dL >>> 22) + 0x0d + (cL >>> 27);
				cL &= 0x7ffffff; cH &= 31;
				t = (eL >>> 2) | ((eH & 3) << 25); eH = (eH >>> 2) | ((eL & 3) << 3); eL = t;

				bL += (dL ^ eL ^ aL) + WL[i + 3] + (((cL & 0x3fffff) << 5) | cH) + 0x06d9eba1;
				bH += (dH ^ eH ^ aH) + WH[i + 3] + (cL >>> 22) + 0x0d + (bL >>> 27);
				bL &= 0x7ffffff; bH &= 31;
				t = (dL >>> 2) | ((dH & 3) << 25); dH = (dH >>> 2) | ((dL & 3) << 3); dL = t;

				aL += (cL ^ dL ^ eL) + WL[i + 4] + (((bL & 0x3fffff) << 5) | bH) + 0x06d9eba1;
				aH += (cH ^ dH ^ eH) + WH[i + 4] + (bL >>> 22) + 0x0d + (aL >>> 27);
				aL &= 0x7ffffff; aH &= 31;
				t = (cL >>> 2) | ((cH & 3) << 25); cH = (cH >>> 2) | ((cL & 3) << 3); cL = t;
			}
			for (var i = 40; i < 60; i += 5) {
				eL += ((bL & (cL | dL)) | (cL & dL)) + WL[i] + (((aL & 0x3fffff) << 5) | aH) + 0x071bbcdc;
				eH += ((bH & (cH | dH)) | (cH & dH)) + WH[i] + (aL >>> 22) + 0x11 + (eL >>> 27);
				eL &= 0x7ffffff; eH &= 31;
				t = (bL >>> 2) | ((bH & 3) << 25); bH = (bH >>> 2) | ((bL & 3) << 3); bL = t;

				dL += ((aL & (bL | cL)) | (bL & cL)) + WL[i + 1] + (((eL & 0x3fffff) << 5) | eH) + 0x071bbcdc;
				dH += ((aH & (bH | cH)) | (bH & cH)) + WH[i + 1] + (eL >>> 22) + 0x11 + (dL >>> 27);
				dL &= 0x7ffffff; dH &= 31;
				t = (aL >>> 2) | ((aH & 3) << 25); aH = (aH >>> 2) | ((aL & 3) << 3); aL = t;

				cL += ((eL & (aL | bL)) | (aL & bL)) + WL[i + 2] + (((dL & 0x3fffff) << 5) | dH) + 0x071bbcdc;
				cH += ((eH & (aH | bH)) | (aH & bH)) + WH[i + 2] + (dL >>> 22) + 0x11 + (cL >>> 27);
				cL &= 0x7ffffff; cH &= 31;
				t = (eL >>> 2) | ((eH & 3) << 25); eH = (eH >>> 2) | ((eL & 3) << 3); eL = t;

				bL += ((dL & (eL | aL)) | (eL & aL)) + WL[i + 3] + (((cL & 0x3fffff) << 5) | cH) + 0x071bbcdc;
				bH += ((dH & (eH | aH)) | (eH & aH)) + WH[i + 3] + (cL >>> 22) + 0x11 + (bL >>> 27);
				bL &= 0x7ffffff; bH &= 31;
				t = (dL >>> 2) | ((dH & 3) << 25); dH = (dH >>> 2) | ((dL & 3) << 3); dL = t;

				aL += ((cL & (dL | eL)) | (dL & eL)) + WL[i + 4] + (((bL & 0x3fffff) << 5) | bH) + 0x071bbcdc;
				aH += ((cH & (dH | eH)) | (dH & eH)) + WH[i + 4] + (bL >>> 22) + 0x11 + (aL >>> 27);
				aL &= 0x7ffffff; aH &= 31;
				t = (cL >>> 2) | ((cH & 3) << 25); cH = (cH >>> 2) | ((cL & 3) << 3); cL = t;
			}
			for (var i = 60; i < 80; i += 5) {
				eL += (bL ^ cL ^ dL) + WL[i] + (((aL & 0x3fffff) << 5) | aH) + 0x0262c1d6;
				eH += (bH ^ cH ^ dH) + WH[i] + (aL >>> 22) + 0x19 + (eL >>> 27);
				eL &= 0x7ffffff; eH &= 31;
				t = (bL >>> 2) | ((bH & 3) << 25); bH = (bH >>> 2) | ((bL & 3) << 3); bL = t;

				dL += (aL ^ bL ^ cL) + WL[i + 1] + (((eL & 0x3fffff) << 5) | eH) + 0x0262c1d6;
				dH += (aH ^ bH ^ cH) + WH[i + 1] + (eL >>> 22) + 0x19 + (dL >>> 27);
				dL &= 0x7ffffff; dH &= 31;
				t = (aL >>> 2) | ((aH & 3) << 25); aH = (aH >>> 2) | ((aL & 3) << 3); aL = t;

				cL += (eL ^ aL ^ bL) + WL[i + 2] + (((dL & 0x3fffff) << 5) | dH) + 0x0262c1d6;
				cH += (eH ^ aH ^ bH) + WH[i + 2] + (dL >>> 22) + 0x19 + (cL >>> 27);
				cL &= 0x7ffffff; cH &= 31;
				t = (eL >>> 2) | ((eH & 3) << 25); eH = (eH >>> 2) | ((eL & 3) << 3); eL = t;

				bL += (dL ^ eL ^ aL) + WL[i + 3] + (((cL & 0x3fffff) << 5) | cH) + 0x0262c1d6;
				bH += (dH ^ eH ^ aH) + WH[i + 3] + (cL >>> 22) + 0x19 + (bL >>> 27);
				bL &= 0x7ffffff; bH &= 31;
				t = (dL >>> 2) | ((dH & 3) << 25); dH = (dH >>> 2) | ((dL & 3) << 3); dL = t;

				aL += (cL ^ dL ^ eL) + WL[i + 4] + (((bL & 0x3fffff) << 5) | bH) + 0x0262c1d6;
				aH += (cH ^ dH ^ eH) + WH[i + 4] + (bL >>> 22) + 0x19 + (aL >>> 27);
				aL &= 0x7ffffff; aH &= 31;
				t = (cL >>> 2) | ((cH & 3) << 25); cH = (cH >>> 2) | ((cL & 3) << 3); cL = t;
			}
			t = this.H_[0] + aL; this.H_[1] = (this.H_[1] + aH + (t >>> 27)) & 31; this.H_[0] = t & 0x7ffffff;
			t = this.H_[2] + bL; this.H_[3] = (this.H_[3] + bH + (t >>> 27)) & 31; this.H_[2] = t & 0x7ffffff;
			t = this.H_[4] + cL; this.H_[5] = (this.H_[5] + cH + (t >>> 27)) & 31; this.H_[4] = t & 0x7ffffff;
			t = this.H_[6] + dL; this.H_[7] = (this.H_[7] + dH + (t >>> 27)) & 31; this.H_[6] = t & 0x7ffffff;
			t = this.H_[8] + eL; this.H_[9] = (this.H_[9] + eH + (t >>> 27)) & 31; this.H_[8] = t & 0x7ffffff;
		},
		update_std : function(buf, charSize) {
			var tmp00, tmp01, tmp02, tmp03, tmp04, tmp05, tmp06, tmp07, tmp08, tmp09;
			var tmp10, tmp11, tmp12, tmp13, tmp14, tmp15, tmp16, tmp17, tmp18, tmp19;
			var tmp20, tmp21, tmp22, tmp23, tmp24, tmp25, tmp26, tmp27, tmp28, tmp29;
			var tmp30, tmp31, tmp32, tmp33, tmp34, tmp35;
			if (charSize == 1) {
				tmp00 = buf.charCodeAt( 3) | (buf.charCodeAt( 2) << 8) | (buf.charCodeAt( 1) << 16) | (buf.charCodeAt( 0) << 24);
				tmp01 = buf.charCodeAt( 7) | (buf.charCodeAt( 6) << 8) | (buf.charCodeAt( 5) << 16) | (buf.charCodeAt( 4) << 24);
				tmp02 = buf.charCodeAt(11) | (buf.charCodeAt(10) << 8) | (buf.charCodeAt( 9) << 16) | (buf.charCodeAt( 8) << 24);
				tmp03 = buf.charCodeAt(15) | (buf.charCodeAt(14) << 8) | (buf.charCodeAt(13) << 16) | (buf.charCodeAt(12) << 24);
				tmp04 = buf.charCodeAt(19) | (buf.charCodeAt(18) << 8) | (buf.charCodeAt(17) << 16) | (buf.charCodeAt(16) << 24);
				tmp05 = buf.charCodeAt(23) | (buf.charCodeAt(22) << 8) | (buf.charCodeAt(21) << 16) | (buf.charCodeAt(20) << 24);
				tmp06 = buf.charCodeAt(27) | (buf.charCodeAt(26) << 8) | (buf.charCodeAt(25) << 16) | (buf.charCodeAt(24) << 24);
				tmp07 = buf.charCodeAt(31) | (buf.charCodeAt(30) << 8) | (buf.charCodeAt(29) << 16) | (buf.charCodeAt(28) << 24);
				tmp08 = buf.charCodeAt(35) | (buf.charCodeAt(34) << 8) | (buf.charCodeAt(33) << 16) | (buf.charCodeAt(32) << 24);
				tmp09 = buf.charCodeAt(39) | (buf.charCodeAt(38) << 8) | (buf.charCodeAt(37) << 16) | (buf.charCodeAt(36) << 24);
				tmp10 = buf.charCodeAt(43) | (buf.charCodeAt(42) << 8) | (buf.charCodeAt(41) << 16) | (buf.charCodeAt(40) << 24);
				tmp11 = buf.charCodeAt(47) | (buf.charCodeAt(46) << 8) | (buf.charCodeAt(45) << 16) | (buf.charCodeAt(44) << 24);
				tmp12 = buf.charCodeAt(51) | (buf.charCodeAt(50) << 8) | (buf.charCodeAt(49) << 16) | (buf.charCodeAt(48) << 24);
				tmp13 = buf.charCodeAt(55) | (buf.charCodeAt(54) << 8) | (buf.charCodeAt(53) << 16) | (buf.charCodeAt(52) << 24);
				tmp14 = buf.charCodeAt(59) | (buf.charCodeAt(58) << 8) | (buf.charCodeAt(57) << 16) | (buf.charCodeAt(56) << 24);
				tmp15 = buf.charCodeAt(63) | (buf.charCodeAt(62) << 8) | (buf.charCodeAt(61) << 16) | (buf.charCodeAt(60) << 24);
			} else {
				tmp00 = this.swap32(buf.charCodeAt( 0) | (buf.charCodeAt( 1) << 16));
				tmp01 = this.swap32(buf.charCodeAt( 2) | (buf.charCodeAt( 3) << 16));
				tmp02 = this.swap32(buf.charCodeAt( 4) | (buf.charCodeAt( 5) << 16));
				tmp03 = this.swap32(buf.charCodeAt( 6) | (buf.charCodeAt( 7) << 16));
				tmp04 = this.swap32(buf.charCodeAt( 8) | (buf.charCodeAt( 9) << 16));
				tmp05 = this.swap32(buf.charCodeAt(10) | (buf.charCodeAt(11) << 16));
				tmp06 = this.swap32(buf.charCodeAt(12) | (buf.charCodeAt(13) << 16));
				tmp07 = this.swap32(buf.charCodeAt(14) | (buf.charCodeAt(15) << 16));
				tmp08 = this.swap32(buf.charCodeAt(16) | (buf.charCodeAt(17) << 16));
				tmp09 = this.swap32(buf.charCodeAt(18) | (buf.charCodeAt(19) << 16));
				tmp10 = this.swap32(buf.charCodeAt(20) | (buf.charCodeAt(21) << 16));
				tmp11 = this.swap32(buf.charCodeAt(22) | (buf.charCodeAt(23) << 16));
				tmp12 = this.swap32(buf.charCodeAt(24) | (buf.charCodeAt(25) << 16));
				tmp13 = this.swap32(buf.charCodeAt(26) | (buf.charCodeAt(27) << 16));
				tmp14 = this.swap32(buf.charCodeAt(28) | (buf.charCodeAt(29) << 16));
				tmp15 = this.swap32(buf.charCodeAt(30) | (buf.charCodeAt(31) << 16));
			}
			var a = this.H_[0];
			var b = this.H_[1];
			var c = this.H_[2];
			var d = this.H_[3];
			var e = this.H_[4];
			var const0 = 0x5a827999;
			var const1 = 0x6ed9eba1;
			var const2 = 0x8f1bbcdc;
			var const3 = 0xca62c1d6;

			var t;

			t = tmp13 ^ tmp08 ^ tmp02 ^ tmp00; tmp16 = (t << 1) | (t >>> 31);
			t = tmp14 ^ tmp09 ^ tmp03 ^ tmp01; tmp17 = (t << 1) | (t >>> 31);
			t = tmp15 ^ tmp10 ^ tmp04 ^ tmp02; tmp18 = (t << 1) | (t >>> 31);
			t = tmp16 ^ tmp11 ^ tmp05 ^ tmp03; tmp19 = (t << 1) | (t >>> 31);

			e += ((a << 5) | (a >>> 27)) + ((b & c) | (~b & d)) + tmp00 + const0; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & b) | (~a & c)) + tmp01 + const0; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & a) | (~e & b)) + tmp02 + const0; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & e) | (~d & a)) + tmp03 + const0; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & d) | (~c & e)) + tmp04 + const0; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + ((b & c) | (~b & d)) + tmp05 + const0; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & b) | (~a & c)) + tmp06 + const0; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & a) | (~e & b)) + tmp07 + const0; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & e) | (~d & a)) + tmp08 + const0; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & d) | (~c & e)) + tmp09 + const0; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + ((b & c) | (~b & d)) + tmp10 + const0; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & b) | (~a & c)) + tmp11 + const0; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & a) | (~e & b)) + tmp12 + const0; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & e) | (~d & a)) + tmp13 + const0; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & d) | (~c & e)) + tmp14 + const0; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + ((b & c) | (~b & d)) + tmp15 + const0; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & b) | (~a & c)) + tmp16 + const0; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & a) | (~e & b)) + tmp17 + const0; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & e) | (~d & a)) + tmp18 + const0; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & d) | (~c & e)) + tmp19 + const0; c = (c << 30) | (c >>> 2);

			t = tmp17 ^ tmp12 ^ tmp06 ^ tmp04; tmp20 = (t << 1) | (t >>> 31);
			t = tmp18 ^ tmp13 ^ tmp07 ^ tmp05; tmp21 = (t << 1) | (t >>> 31);
			t = tmp19 ^ tmp14 ^ tmp08 ^ tmp06; tmp22 = (t << 1) | (t >>> 31);
			t = tmp20 ^ tmp15 ^ tmp09 ^ tmp07; tmp23 = (t << 1) | (t >>> 31);
			t = tmp21 ^ tmp16 ^ tmp10 ^ tmp08; tmp24 = (t << 1) | (t >>> 31);
			t = tmp22 ^ tmp17 ^ tmp11 ^ tmp09; tmp25 = (t << 1) | (t >>> 31);
			t = tmp23 ^ tmp18 ^ tmp12 ^ tmp10; tmp26 = (t << 1) | (t >>> 31);
			t = tmp24 ^ tmp19 ^ tmp13 ^ tmp11; tmp27 = (t << 1) | (t >>> 31);
			t = tmp25 ^ tmp20 ^ tmp14 ^ tmp12; tmp28 = (t << 1) | (t >>> 31);
			t = tmp26 ^ tmp21 ^ tmp15 ^ tmp13; tmp29 = (t << 1) | (t >>> 31);
			t = tmp27 ^ tmp22 ^ tmp16 ^ tmp14; tmp30 = (t << 1) | (t >>> 31);
			t = tmp28 ^ tmp23 ^ tmp17 ^ tmp15; tmp31 = (t << 1) | (t >>> 31);
			t = tmp29 ^ tmp24 ^ tmp18 ^ tmp16; tmp32 = (t << 1) | (t >>> 31);
			t = tmp30 ^ tmp25 ^ tmp19 ^ tmp17; tmp33 = (t << 1) | (t >>> 31);
			t = tmp31 ^ tmp26 ^ tmp20 ^ tmp18; tmp34 = (t << 1) | (t >>> 31);
			t = tmp32 ^ tmp27 ^ tmp21 ^ tmp19; tmp35 = (t << 1) | (t >>> 31);
			t = tmp33 ^ tmp28 ^ tmp22 ^ tmp20; tmp00 = (t << 1) | (t >>> 31);
			t = tmp34 ^ tmp29 ^ tmp23 ^ tmp21; tmp01 = (t << 1) | (t >>> 31);
			t = tmp35 ^ tmp30 ^ tmp24 ^ tmp22; tmp02 = (t << 1) | (t >>> 31);
			t = tmp00 ^ tmp31 ^ tmp25 ^ tmp23; tmp03 = (t << 1) | (t >>> 31);

			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp20 + const1; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp21 + const1; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp22 + const1; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp23 + const1; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp24 + const1; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp25 + const1; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp26 + const1; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp27 + const1; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp28 + const1; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp29 + const1; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp30 + const1; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp31 + const1; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp32 + const1; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp33 + const1; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp34 + const1; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp35 + const1; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp00 + const1; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp01 + const1; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp02 + const1; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp03 + const1; c = (c << 30) | (c >>> 2);
                                                         
			t = tmp01 ^ tmp32 ^ tmp26 ^ tmp24; tmp04 = (t << 1) | (t >>> 31);
			t = tmp02 ^ tmp33 ^ tmp27 ^ tmp25; tmp05 = (t << 1) | (t >>> 31);
			t = tmp03 ^ tmp34 ^ tmp28 ^ tmp26; tmp06 = (t << 1) | (t >>> 31);
			t = tmp04 ^ tmp35 ^ tmp29 ^ tmp27; tmp07 = (t << 1) | (t >>> 31);
			t = tmp05 ^ tmp00 ^ tmp30 ^ tmp28; tmp08 = (t << 1) | (t >>> 31);
			t = tmp06 ^ tmp01 ^ tmp31 ^ tmp29; tmp09 = (t << 1) | (t >>> 31);
			t = tmp07 ^ tmp02 ^ tmp32 ^ tmp30; tmp10 = (t << 1) | (t >>> 31);
			t = tmp08 ^ tmp03 ^ tmp33 ^ tmp31; tmp11 = (t << 1) | (t >>> 31);
			t = tmp09 ^ tmp04 ^ tmp34 ^ tmp32; tmp12 = (t << 1) | (t >>> 31);
			t = tmp10 ^ tmp05 ^ tmp35 ^ tmp33; tmp13 = (t << 1) | (t >>> 31);
			t = tmp11 ^ tmp06 ^ tmp00 ^ tmp34; tmp14 = (t << 1) | (t >>> 31);
			t = tmp12 ^ tmp07 ^ tmp01 ^ tmp35; tmp15 = (t << 1) | (t >>> 31);
			t = tmp13 ^ tmp08 ^ tmp02 ^ tmp00; tmp16 = (t << 1) | (t >>> 31);
			t = tmp14 ^ tmp09 ^ tmp03 ^ tmp01; tmp17 = (t << 1) | (t >>> 31);
			t = tmp15 ^ tmp10 ^ tmp04 ^ tmp02; tmp18 = (t << 1) | (t >>> 31);
			t = tmp16 ^ tmp11 ^ tmp05 ^ tmp03; tmp19 = (t << 1) | (t >>> 31);
			t = tmp17 ^ tmp12 ^ tmp06 ^ tmp04; tmp20 = (t << 1) | (t >>> 31);
			t = tmp18 ^ tmp13 ^ tmp07 ^ tmp05; tmp21 = (t << 1) | (t >>> 31);
			t = tmp19 ^ tmp14 ^ tmp08 ^ tmp06; tmp22 = (t << 1) | (t >>> 31);
			t = tmp20 ^ tmp15 ^ tmp09 ^ tmp07; tmp23 = (t << 1) | (t >>> 31);

			e += ((a << 5) | (a >>> 27)) + ((b & (c | d)) | (c & d)) + tmp04 + const2; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & (b | c)) | (b & c)) + tmp05 + const2; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & (a | b)) | (a & b)) + tmp06 + const2; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & (e | a)) | (e & a)) + tmp07 + const2; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & (d | e)) | (d & e)) + tmp08 + const2; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + ((b & (c | d)) | (c & d)) + tmp09 + const2; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & (b | c)) | (b & c)) + tmp10 + const2; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & (a | b)) | (a & b)) + tmp11 + const2; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & (e | a)) | (e & a)) + tmp12 + const2; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & (d | e)) | (d & e)) + tmp13 + const2; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + ((b & (c | d)) | (c & d)) + tmp14 + const2; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & (b | c)) | (b & c)) + tmp15 + const2; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & (a | b)) | (a & b)) + tmp16 + const2; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & (e | a)) | (e & a)) + tmp17 + const2; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & (d | e)) | (d & e)) + tmp18 + const2; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + ((b & (c | d)) | (c & d)) + tmp19 + const2; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + ((a & (b | c)) | (b & c)) + tmp20 + const2; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + ((e & (a | b)) | (a & b)) + tmp21 + const2; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + ((d & (e | a)) | (e & a)) + tmp22 + const2; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + ((c & (d | e)) | (d & e)) + tmp23 + const2; c = (c << 30) | (c >>> 2);

			t = tmp21 ^ tmp16 ^ tmp10 ^ tmp08; tmp24 = (t << 1) | (t >>> 31);
			t = tmp22 ^ tmp17 ^ tmp11 ^ tmp09; tmp25 = (t << 1) | (t >>> 31);
			t = tmp23 ^ tmp18 ^ tmp12 ^ tmp10; tmp26 = (t << 1) | (t >>> 31);
			t = tmp24 ^ tmp19 ^ tmp13 ^ tmp11; tmp27 = (t << 1) | (t >>> 31);
			t = tmp25 ^ tmp20 ^ tmp14 ^ tmp12; tmp28 = (t << 1) | (t >>> 31);
			t = tmp26 ^ tmp21 ^ tmp15 ^ tmp13; tmp29 = (t << 1) | (t >>> 31);
			t = tmp27 ^ tmp22 ^ tmp16 ^ tmp14; tmp30 = (t << 1) | (t >>> 31);
			t = tmp28 ^ tmp23 ^ tmp17 ^ tmp15; tmp31 = (t << 1) | (t >>> 31);
			t = tmp29 ^ tmp24 ^ tmp18 ^ tmp16; tmp32 = (t << 1) | (t >>> 31);
			t = tmp30 ^ tmp25 ^ tmp19 ^ tmp17; tmp33 = (t << 1) | (t >>> 31);
			t = tmp31 ^ tmp26 ^ tmp20 ^ tmp18; tmp34 = (t << 1) | (t >>> 31);
			t = tmp32 ^ tmp27 ^ tmp21 ^ tmp19; tmp35 = (t << 1) | (t >>> 31);
			t = tmp33 ^ tmp28 ^ tmp22 ^ tmp20; tmp00 = (t << 1) | (t >>> 31);
			t = tmp34 ^ tmp29 ^ tmp23 ^ tmp21; tmp01 = (t << 1) | (t >>> 31);
			t = tmp35 ^ tmp30 ^ tmp24 ^ tmp22; tmp02 = (t << 1) | (t >>> 31);
			t = tmp00 ^ tmp31 ^ tmp25 ^ tmp23; tmp03 = (t << 1) | (t >>> 31);
			t = tmp01 ^ tmp32 ^ tmp26 ^ tmp24; tmp04 = (t << 1) | (t >>> 31);
			t = tmp02 ^ tmp33 ^ tmp27 ^ tmp25; tmp05 = (t << 1) | (t >>> 31);
			t = tmp03 ^ tmp34 ^ tmp28 ^ tmp26; tmp06 = (t << 1) | (t >>> 31);
			t = tmp04 ^ tmp35 ^ tmp29 ^ tmp27; tmp07 = (t << 1) | (t >>> 31);

			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp24 + const3; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp25 + const3; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp26 + const3; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp27 + const3; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp28 + const3; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp29 + const3; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp30 + const3; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp31 + const3; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp32 + const3; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp33 + const3; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp34 + const3; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp35 + const3; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp00 + const3; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp01 + const3; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp02 + const3; c = (c << 30) | (c >>> 2);
			e += ((a << 5) | (a >>> 27)) + (b ^ c ^ d) + tmp03 + const3; b = (b << 30) | (b >>> 2);
			d += ((e << 5) | (e >>> 27)) + (a ^ b ^ c) + tmp04 + const3; a = (a << 30) | (a >>> 2);
			c += ((d << 5) | (d >>> 27)) + (e ^ a ^ b) + tmp05 + const3; e = (e << 30) | (e >>> 2);
			b += ((c << 5) | (c >>> 27)) + (d ^ e ^ a) + tmp06 + const3; d = (d << 30) | (d >>> 2);
			a += ((b << 5) | (b >>> 27)) + (c ^ d ^ e) + tmp07 + const3; c = (c << 30) | (c >>> 2);

			this.H_[0] = (this.H_[0] + a) & 0xffffffff;
			this.H_[1] = (this.H_[1] + b) & 0xffffffff;
			this.H_[2] = (this.H_[2] + c) & 0xffffffff;
			this.H_[3] = (this.H_[3] + d) & 0xffffffff;
			this.H_[4] = (this.H_[4] + e) & 0xffffffff;
		},

		fillzero : function(size) {
			var buf = "";
			for (var i = 0; i < size; i++) {
				buf += "\x00";
			}
			return buf;
		},

		main : function(buf, bufSize, update, self, charSize) {
			if (charSize == 1) {
				var totalBitSize = bufSize * 8;
				while (bufSize >= 64) {
					self[update](buf, charSize);
					buf = buf.substr(64);
					bufSize -= 64;
				}
				buf +="\x80";
				if (bufSize >= 56) {
					buf += this.fillzero(63 - bufSize);
					self[update](buf, charSize);
					buf = this.fillzero(56);
				} else {
					buf += this.fillzero(55 - bufSize);
				}
				buf += "\x00\x00\x00\x00"; // in stead of (totalBitSize) >> 32
				buf += String.fromCharCode(totalBitSize >>> 24, (totalBitSize >>> 16) & 0xff, (totalBitSize >>> 8) & 0xff, totalBitSize & 0xff);
				self[update](buf, charSize);
			} else {
				/* charSize == 2 */
				var totalBitSize = bufSize * 16;
				while (bufSize >= 32) {
					self[update](buf, charSize);
					buf = buf.substr(32);
					bufSize -= 32;
				}
				buf +="\x80";
				if (bufSize >= 28) {
					buf += this.fillzero(31 - bufSize);
					self[update](buf, charSize);
					buf = this.fillzero(28);
				} else {
					buf += this.fillzero(27 - bufSize);
				}
				buf += "\x00\x00"; // in stead of (totalBitSize) >> 32
				totalBitSize = this.swap32(totalBitSize);
				buf += String.fromCharCode(totalBitSize & 65535, totalBitSize >>> 16);
				self[update](buf, charSize);
			}
		},

		VERSION : "1.0",
		BY_ASCII : 0,
		BY_UTF16 : 1,

		calc_Fx : function(msg, mode) {
			var charSize = (arguments.length == 2 && mode == this.BY_UTF16) ? 2 : 1;
			this.H_ = [0x07452301, 0x0c, 0x07cdab89, 0x1d, 0x00badcfe, 0x13, 0x00325476, 0x02, 0x03d2e1f0, 0x18];
			this.main(msg, msg.length, "update_Fx", this, charSize);
			var ret = "";
			for (var i = 0; i < 5; i++) {
				ret += this.int32toBE((this.H_[2 * i + 1] << 27) + this.H_[2 * i]);
			}
			return ret;
		},
		calc_std : function(msg, mode) {
			var charSize = (arguments.length == 2 && mode == this.BY_UTF16) ? 2 : 1;
			this.H_ = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0];
			this.main(msg, msg.length, "update_std", this, charSize);
			var ret = "";
			for (var i = 0; i < 5; i++) {
				ret += this.int32toBE(this.H_[i]);
			}
			return ret;
		}
	} // end of SHA1
}; // end of CybozuLabs

new function() {
	CybozuLabs.SHA1.calc = navigator.userAgent.match(/Firefox/) ? CybozuLabs.SHA1.calc_Fx : CybozuLabs.SHA1.calc_std;
};
