package com.stripe.ctf.instantcodesearch
import org.jboss.netty.handler.codec.http.HttpResponseStatus

class HttpException(val code : HttpResponseStatus, val message : String) extends RuntimeException(message)
class NotFoundException(message : String) extends HttpException(HttpResponseStatus.NOT_FOUND, message)
class BadRequestException(message : String) extends HttpException(HttpResponseStatus.BAD_REQUEST, message)
