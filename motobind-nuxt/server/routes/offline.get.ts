import { defineEventHandler, sendRedirect } from 'h3'

export default defineEventHandler((event) => sendRedirect(event, '/offline.html', 302))
