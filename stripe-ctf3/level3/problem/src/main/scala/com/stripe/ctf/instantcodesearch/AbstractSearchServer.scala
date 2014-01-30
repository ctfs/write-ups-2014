package com.stripe.ctf.instantcodesearch

import java.io._
import org.apache.commons.lang.StringUtils
import com.twitter.finagle.Service
import com.twitter.finagle.http.{Http => HttpCodec}
import com.twitter.finagle.builder.ServerBuilder
import com.twitter.server.TwitterServer
import com.twitter.util.Future
import java.net.InetSocketAddress
import org.jboss.netty.buffer.ChannelBuffers.copiedBuffer
import org.jboss.netty.handler.codec.http._
import org.jboss.netty.util.CharsetUtil.UTF_8
import scala.collection.JavaConverters._
import scala.collection.Map
import scala.collection.mutable.Buffer

abstract class AbstractSearchServer(port: Int, id: Int) extends TwitterServer {
  def query(q: String): Future[HttpResponse]
  def index(path: String): Future[HttpResponse]
  def healthcheck(): Future[HttpResponse]
  def isIndexed(): Future[HttpResponse]

  def handle(request: HttpRequest): Future[HttpResponse] = {
    val decoder = new QueryStringDecoder(request.getUri)
    val params = decoder.getParameters.asScala.mapValues {_.asScala}

    try {
      decoder.getPath() match {
        case "/index" => index(getParam(params, "path"))
        case "/" => query(getParam(params, "q"))
        case "/healthcheck" => healthcheck()
        case "/isIndexed" => isIndexed()
        case path => throw new NotFoundException(path + " not found")
      }
    }
    catch {
      case err: HttpException => Future.value(
        errorResponse(err.code, err.message)
      )
      case _: Exception => {
        Future.value(
          errorResponse(
            HttpResponseStatus.INTERNAL_SERVER_ERROR,
            "Something went wrong"
          )
        )
      }
    }
  }

  def httpResponse(message: String, code: HttpResponseStatus): HttpResponse = {
    val response = new DefaultHttpResponse(HttpVersion.HTTP_1_1, code)
    response.setContent(copiedBuffer(message, UTF_8))

    response
  }

  def successResponse(): HttpResponse = {
    val content = "{\"success\": true}"
    httpResponse(content, HttpResponseStatus.OK)
  }

  def querySuccessResponse(results: List[Match]): HttpResponse = {
    val response = new DefaultHttpResponse(HttpVersion.HTTP_1_1, HttpResponseStatus.OK)
    val resultString = results
      .map {r => "\"" + r.path + ":" + r.line + "\""}
      .mkString("[", ",\n", "]")
    val content = "{\"success\": true,\n \"results\": " + resultString + "}"
    response.setContent(copiedBuffer(content, UTF_8))

    response
  }

  def errorResponse(code: HttpResponseStatus, message: String) = {
    val content = "{\"success\": false, \"error\": \"" + message + "\"}"
    httpResponse(content, code)
  }

  def getParam(params: Map[String, Buffer[String]], key: String) : String = {
    params.get(key)
      .flatMap { _.headOption }
      .getOrElse {
        throw new BadRequestException("Parameter '" + key + "' not specified")
      }
  }

  def readIndex(path: String): Index = {
    new ObjectInputStream(
      new FileInputStream(new File(path))
    ).readObject.asInstanceOf[Index]
  }

  val server = ServerBuilder()
    .codec(HttpCodec())
    .bindTo(new InetSocketAddress(port))
    .name("server-" + id)
    .build(new Service[HttpRequest, HttpResponse] {
      override def apply(request : HttpRequest) : Future[HttpResponse] = {
        handle(request)
      }
    })
}
