-- Resuelve referencias Quarto @fig-* en la salida autónoma de Pandoc.

local figure_numbers = {}

local function has_class(element, class_name)
  for _, class in ipairs(element.classes or {}) do
    if class == class_name then return true end
  end
  return false
end

local function prefix_caption(figure, label)
  if not FORMAT:match("html") then return figure end
  local prefix = {
    pandoc.Strong({pandoc.Str("Figura " .. label .. ".")}),
    pandoc.Space()
  }
  if #figure.caption.long == 0 then
    figure.caption.long = {pandoc.Plain(prefix)}
    return figure
  end
  local first = figure.caption.long[1]
  if first.t == "Plain" or first.t == "Para" then
    local content = {}
    for _, inline in ipairs(prefix) do table.insert(content, inline) end
    for _, inline in ipairs(first.content) do table.insert(content, inline) end
    first.content = content
  else
    table.insert(figure.caption.long, 1, pandoc.Plain(prefix))
  end
  return figure
end

function Pandoc(doc)
  local chapter = 0
  local figure_in_chapter = 0

  for _, block in ipairs(doc.blocks) do
    if block.t == "Header" and block.level == 1 and not has_class(block, "unnumbered") then
      chapter = chapter + 1
      figure_in_chapter = 0
    elseif block.t == "Figure" and block.identifier and block.identifier ~= "" then
      figure_in_chapter = figure_in_chapter + 1
      figure_numbers[block.identifier] = tostring(chapter) .. "." .. tostring(figure_in_chapter)
    end
  end

  doc = doc:walk({
    Cite = function(cite)
      if #cite.citations == 1 then
        local id = cite.citations[1].id
        local number = figure_numbers[id]
        if number then
          return pandoc.Link({pandoc.Str("Figura " .. number)}, "#" .. id)
        end
      end
      return cite
    end,
    Link = function(link)
      local anchor = link.target:match("^[^#]+%.qmd#(.+)$")
      if anchor then
        link.target = "#" .. anchor
        return link
      end
      return link
    end,
    Figure = function(figure)
      local number = figure_numbers[figure.identifier]
      if number then return prefix_caption(figure, number) end
      return figure
    end
  })

  return doc
end
