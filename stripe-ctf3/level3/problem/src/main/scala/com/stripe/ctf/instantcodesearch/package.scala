package com.stripe.ctf

import java.io._
import java.nio.file._
import java.nio.charset._


package object instantcodesearch {
  val utf8Decoder = Charset.forName("UTF-8").newDecoder().
    onMalformedInput(CodingErrorAction.REPORT).
    onUnmappableCharacter(CodingErrorAction.REPORT)

  def slurp(r : Reader) : String = {
    val sb = new StringBuilder
    val buf = new Array[Char](4096)
    var n = 0
    while (n != -1) {
      n = r.read(buf)
      if (n > 0)
        sb.appendAll(buf, 0, n)
    }
    return sb.toString
  }

  def slurp(p : Path) : String = {
    val r = new InputStreamReader(new ByteArrayInputStream(Files.readAllBytes(p)), utf8Decoder)
    return slurp(r)
  }
}
